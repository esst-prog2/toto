"""Independent raw reconciliation of proposed early Turkish date recovery.

Uses its own HTMLParser and positional source matching. No production recovery,
fixture, mapping resolver, ID or serialization helper is imported. Historical
season-bound correspondence declarations are shared reviewed policy input.
"""
from collections import Counter, defaultdict
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import argparse
import hashlib
import json
import re
import tempfile

from scripts import validate_turkish_super_lig_structure as original_reader

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/private/turkey/super_lig/early_date_recovery"
OUTPUT = PRIVATE / "proposed"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def enc(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()


def load(path):
    return json.loads(path.read_bytes())


def check(value, message):
    if not value:
        raise ValueError(message)


class Rows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.cell = None
        self.items = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr" and attrs.get("class") == "haftaninMaclariTr":
            check(not self.active, "Nested target fixture row")
            self.active = True
            self.values = {}
            self.ids = set()
            self.first = self.getpos()[0]
        if self.active and tag == "td":
            self.cell = attrs.get("class")
            self.values[self.cell] = []
        if self.active and tag == "a":
            self.ids.update(re.findall(r"macid=(\d+)", attrs.get("href", ""), re.I))

    def handle_data(self, data):
        if self.active and self.cell:
            self.values[self.cell].append(data)

    def handle_endtag(self, tag):
        if self.active and tag == "td":
            self.cell = None
        if self.active and tag == "tr":
            check(len(self.ids) == 1, "Missing primary fixture ID")
            self.items.append(dict(first=self.first, last=self.getpos()[0],
                                   values={k: " ".join("".join(v).split()) for k, v in self.values.items()},
                                   identity=next(iter(self.ids))))
            self.active = False


class Detail(HTMLParser):
    """Official match-panel extraction independent of production's regexes."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.field = self.tag = None
        self.fields = {}

    def handle_starttag(self, tag, attrs):
        name = dict(attrs).get("id", "")
        marker = "_MacBilgiDisplay1_dtMacBilgisi_"
        if marker in name:
            suffix = name.split(marker, 1)[1]
            if suffix in {"lnkTakim1", "lnkTakim2", "lblTakim1Skor", "Label12", "lblTarih", "lblOrganizasyonAdi"}:
                check(suffix not in self.fields, "Duplicate official panel field")
                self.fields[suffix] = []
                self.field, self.tag = suffix, tag

    def handle_data(self, data):
        if self.field:
            self.fields[self.field].append(data)

    def handle_endtag(self, tag):
        if self.field and tag == self.tag:
            self.field = self.tag = None

    def result(self):
        z = {k: " ".join("".join(v).split()) for k, v in self.fields.items()}
        check(len(z) == 6 and "Profesyonel Takım" in z["lblOrganizasyonAdi"] and
              "Lig" in z["lblOrganizasyonAdi"], "Wrong/missing professional competition panel")
        d, m, y = map(int, z["lblTarih"].split(" - ")[0].split("."))
        return dict(date=date(y, m, d).isoformat(), home=z["lnkTakim1"], away=z["lnkTakim2"],
                    score=[int(z["lblTakim1Skor"]), int(z["Label12"])],
                    competition=z["lblOrganizasyonAdi"])


def parse(raw, item):
    parser = Rows()
    text = raw.decode("iso-8859-9")
    parser.feed(text)
    check(not parser.active and len(parser.items) == 8, "Truncated/incorrect primary round")
    y = int(item["season"][:4])
    check(f"{y}-{y+1} Sezonu" in text, "Wrong primary season")
    check(re.findall(r">(\d+)\.Hafta<", text) == [str(item["round"])], "Wrong primary round")
    physical = raw.splitlines(keepends=True)
    rows = []
    for fixture in parser.items:
        v = fixture["values"]
        check(set(v) == {"haftaninMaclariTarih", "haftaninMaclariEv", "haftaninMaclariSkor",
                         "haftaninMaclariDeplasman", "haftaninMaclariDetay"}, "Primary field schema")
        literal = v["haftaninMaclariTarih"].split()[0]
        dd, mm, yyyy = map(int, literal.split("."))
        day = date(yyyy, mm, dd)
        check(date(y, 7, 1) <= day <= date(y+1, 6, 30), "Primary date outside season")
        parts = v["haftaninMaclariSkor"].split("-")
        check(len(parts) == 2 and all(p.strip().isdigit() for p in parts), "Primary result absent")
        block = b"".join(physical[fixture["first"]-1:fixture["last"]])
        # Find the literal target row within physical boundary lines, independently
        # of production's whole-document byte-range expression.
        offset = block.index(b'<tr class="haftaninMaclariTr">')
        stop = block.index(b"</tr>", offset) + len(b"</tr>")
        byte_start = sum(map(len, physical[:fixture["first"]-1])) + offset
        rows.append(dict(season=item["season"], round=item["round"], date=day.isoformat(),
                         home=v["haftaninMaclariEv"], away=v["haftaninMaclariDeplasman"],
                         score=list(map(lambda s: int(s.strip()), parts)),
                         tff_match_id=fixture["identity"], line=fixture["first"], end_line=fixture["last"],
                         byte_start=byte_start, byte_end=byte_start+stop-offset,
                         record_sha256=sha(block[offset:stop]), source_sha256=sha(raw),
                         source_url=item["url"], source=str((PRIVATE/item["path"]).relative_to(ROOT)),
                         stage="REGULAR_SEASON"))
    return rows


def validate(directory=OUTPUT):
    affected = load(directory / "affected_events.json")
    supplemental = load(directory / "supplemental_decisions.json")
    report = load(directory / "recovery_assessment.json")
    frozen = load(PRIVATE.parent / "phase3/accepted/decision_registry.json")
    inventory = load(PRIVATE.parent / "phase2/validated/source_inventory.json")
    observations = {r["source_id"]: r for r in inventory["observations"]}
    reconstructed = []
    for rec in inventory["catalogue"]:
        if rec["root_path"].endswith(("/tur93.html", "/tur94.html")):
            raw = (ROOT / rec["root_path"]).read_bytes()
            check(sha(raw) == rec["sha256"], "Original RSSSF bytes changed")
            reconstructed.extend(original_reader.parse_rsssf(raw, rec)[0])
    check(len(reconstructed) == 480, "Independent original extraction incomplete")
    for row in reconstructed:
        for key in ("source_id", "source_sha256", "line", "end_line", "cell", "physical_sha256",
                    "season", "stage", "home", "away", "hg", "ag", "date", "round"):
            check(row[key] == observations[row["source_id"]][key], "Original source-field mismatch")
    byid = {d["event_id"]: d for d in frozen["decisions"]}
    target_ids = {d["event_id"] for d in frozen["decisions"] if d["disposition"] == "HOLD_OUT"
                  and d["season"] in ("1992/1993", "1993/1994")}
    check(len(target_ids) == 480, "Frozen target count")
    check(len(affected["events"]) == 480 and {r["event_id"] for r in affected["events"]} == target_ids,
          "Affected event extraction incomplete")
    check(affected["untouched_other_hold_event_ids"] == sorted(
        d["event_id"] for d in frozen["decisions"] if d["disposition"] == "HOLD_OUT" and d["event_id"] not in target_ids),
        "Other HOLD OUT population altered")
    for target in affected["events"]:
        check(target["frozen_decision"] == byid[target["event_id"]], "Frozen decision changed")
        check(target["source_observation"] == observations[target["frozen_decision"]["source_ids"][0]],
              "Original observation lost")
    for distribution in affected["distributions"]:
        source_rows = [observations[byid[eid]["source_ids"][0]] for eid in target_ids
                       if byid[eid]["season"] == distribution["season"]]
        check(distribution["events"] == len(source_rows) == 240, "Extraction distribution count")
        check(distribution["raw_team_participations"] == dict(Counter(r[k] for r in source_rows for k in ("home", "away"))),
              "Raw team distribution changed")
        check(distribution["reported_score_counts"] == dict(Counter(r["hg"]+"-"+r["ag"] for r in source_rows)),
              "Original reported-score distribution changed")
        check(distribution["date_information"] == dict(Counter("NO_DATE" if not r.get("nominal_date_heading") else
              "ROUND_RANGE" if "-" in r["nominal_date_heading"] else "SINGLE_DAY_NOMINAL_HEADING" for r in source_rows)),
              "Date-context distribution changed")
    plan = load(PRIVATE / "fixture_plan.json")
    mapping = load(PRIVATE / "identity_config.json")["source_season_maps"]
    primary = []
    permission = load(PRIVATE / "metadata/tff_terms.html.provenance.json")
    check(sha((PRIVATE / "metadata/tff_terms.html").read_bytes()) == permission["sha256"], "Permission original changed")
    for item in plan["items"]:
        raw = (PRIVATE/item["path"]).read_bytes()
        receipt = load(PRIVATE/(item["path"]+".provenance.json"))
        check(receipt["status"] == 200 and receipt["url"] == receipt["final_url"] == item["url"],
              "Primary acquisition provenance failed")
        check(receipt["sha256"] == sha(raw) and receipt["bytes"] == len(raw) <= item["max_bytes"],
              "Primary byte binding failed")
        check(item["permission_sha256"] == permission["sha256"] and bool(receipt["retrieved_at_utc"]),
              "Permission/time binding failed")
        primary.extend(parse(raw, item))
    repairs = load(PRIVATE / "repair_rules.json")["cases"]
    details = {}
    for item in load(PRIVATE / "case_evidence_plan.json")["items"]:
        raw = (PRIVATE/item["path"]).read_bytes()
        receipt = load(PRIVATE/(item["path"]+".provenance.json"))
        check(receipt["sha256"] == sha(raw) and receipt["bytes"] == len(raw) and
              receipt["url"] == receipt["final_url"] == item["url"] and
              receipt["permission_sha256"] == permission["sha256"] and receipt["status"] == 200,
              "Match-detail provenance binding failed")
        panel = Detail()
        panel.feed(raw.decode("iso-8859-9"))
        details[item["tff_match_id"]] = dict(panel.result(), source=str((PRIVATE/item["path"]).relative_to(ROOT)),
            source_sha256=sha(raw), url=item["url"], retrieved_at_utc=receipt["retrieved_at_utc"])
    check(len(primary) == 480 and len({r["tff_match_id"] for r in primary}) == 480, "Primary event duplication/gap")
    for season in mapping:
        subset = [r for r in primary if r["season"] == season]
        check(len(subset) == 240 and len({r["home"] for r in subset}) == 16, "Primary season structure")
        pairs = Counter((r["home"], r["away"]) for r in subset)
        check(len(pairs) == 240 and set(pairs.values()) == {1}, "Primary directed pairing duplication")
        check(set(Counter(r[k] for r in subset for k in ["home", "away"]).values()) == {30},
              "Primary club participation mismatch")
    # Separate season totals in the old RSSSF tables corroborate the repaired
    # fixture population; tables never supply missing dates or invent fixtures.
    table_maps = load(PRIVATE / "aggregate_identity_config.json")["maps"]
    table_checks = 0
    for season, names in table_maps.items():
        stats = defaultdict(lambda: Counter(games=0, won=0, drawn=0, lost=0, gf=0, ga=0, points=0))
        for fixture in primary:
            if fixture["season"] != season:
                continue
            for club, gf, ga in [(fixture["home"], *fixture["score"]),
                                 (fixture["away"], *reversed(fixture["score"]))]:
                stats[club].update(games=1, gf=gf, ga=ga, won=int(gf>ga), drawn=int(gf==ga),
                                   lost=int(gf<ga), points=3*int(gf>ga)+int(gf==ga))
        seen = set()
        for row in inventory["aggregate_tables"]:
            if row["season"] != season:
                continue
            club = names[row["club"]]
            for key in ["games", "won", "drawn", "lost", "gf", "ga", "points"]:
                check(stats[club][key] == row[key], "Independent final-table totals disagree")
            seen.add(club)
        check(len(seen) == 16, "Incomplete final-table reconciliation")
        table_checks += len(seen)
    results = supplemental["decisions"]
    check(len(results) == 480 and len({d["event_id"] for d in results}) == 480 and
          {d["event_id"] for d in results} == target_ids, "Supplement population incomplete")
    primary_pair = defaultdict(list)
    for r in primary:
        primary_pair[(r["season"], r["home"], r["away"])].append(r)
    expected = {}
    tentative_matches = defaultdict(list)
    for d in results:
        old = byid[d["event_id"]]
        r = observations[old["source_ids"][0]]
        check(d["source_ids"] == old["source_ids"] and d["old_disposition"] == "HOLD_OUT" and
              d["approval_state"] == "PROPOSED_ONLY" and d["old_accepted"] is None, "Silent frozen population expansion")
        check(d["source_observation_sha256"] == sha(enc(r)), "Changed original fields")
        h, a = (mapping[r["season"]].get(r[k]) for k in ["home", "away"])
        candidates = primary_pair[(r["season"], h, a)] if h and a else []
        why = "UNRESOLVED_SOURCE_IDENTITY" if h is None or a is None else (
            "MISSING_OR_AMBIGUOUS_DIRECTED_FIXTURE" if len(candidates) != 1 else
            "SOURCE_SCORE_CONFLICT" if candidates[0]["score"] != [int(r["hg"]), int(r["ag"])] else
            "SOURCE_ROUND_IDENTITY_CONFLICT" if r["round"] and r["round"] != candidates[0]["round"] else
            "PRIMARY_EXPLICIT_DATE_EXACT_FIXTURE_CORRESPONDENCE")
        repair = repairs.get(d["event_id"])
        if repair:
            check(sha(enc(r)) == repair["source_observation_sha256"] and
                  repair["source_id"] == r["source_id"] and
                  repair["physical_sha256"] == r["physical_sha256"], "Unbound source-specific repair")
            check(repair["original_fields"] == {k:r[k] for k in ["home", "away", "hg", "ag", "round"]},
                  "Repair original values lost")
            candidates = [z for z in primary if z["tff_match_id"] == repair["tff_match_id"]]
            check(len(candidates) == 1, "Repair fixture not uniquely supported")
            candidate = candidates[0]
            check(candidate["season"] == r["season"] and
                  (not r["round"] or candidate["round"] == r["round"]), "Repair season/round mismatch")
            detail = details[repair["tff_match_id"]]
            for key in ("date", "home", "away", "score"):
                check(candidate[key] == detail[key] == repair["proposed_fields"][key],
                      "Repair conflicts with official professional panel")
            old_score = [int(r["hg"]), int(r["ag"])]
            if repair["repair_kind"] == "SCORE_CORRECTION":
                check((h, a) == (candidate["home"], candidate["away"]) and old_score != candidate["score"],
                      "Score repair silently changes fixture identity")
            elif repair["repair_kind"] == "OPPONENT_CORRECTION":
                check(h == candidate["home"] and a is not None and a != candidate["away"] and
                      old_score == candidate["score"], "Opponent repair exceeds reviewed scope")
            else:
                check(repair["repair_kind"] == "SOURCE_LABEL_CORRECTION" and h == candidate["home"] and
                      a is None and old_score == candidate["score"], "Unknown/overbroad source-label repair")
            check(d["source_repair"] == repair and d["official_match_detail"] == detail,
                  "Repair audit metadata incomplete")
            why = "REVIEWED_SOURCE_SPECIFIC_REPAIR"
        expected[d["event_id"]] = [why, candidates]
        if why in ("PRIMARY_EXPLICIT_DATE_EXACT_FIXTURE_CORRESPONDENCE", "REVIEWED_SOURCE_SPECIFIC_REPAIR"):
            tentative_matches[candidates[0]["tff_match_id"]].append(d["event_id"])
    for members in tentative_matches.values():
        if len(members) > 1:
            for eid in members:
                expected[eid][0] = "MULTIPLE_FROZEN_EVENTS_FOR_ONE_PRIMARY_FIXTURE"
    included = []
    for d in results:
        why, candidates = expected[d["event_id"]]
        check(d["reason"] == why and d["candidate_fixtures"] == candidates, "Independent candidate correspondence mismatch")
        qualifies = why in ("PRIMARY_EXPLICIT_DATE_EXACT_FIXTURE_CORRESPONDENCE", "REVIEWED_SOURCE_SPECIFIC_REPAIR")
        check(d["proposed_disposition"] == ("INCLUDE" if qualifies else "HOLD_OUT"), "Unsupported proposed disposition")
        check(d["proposed_date"] == (candidates[0]["date"] if qualifies else None), "Unsupported inferred date")
        if qualifies:
            included.append(candidates[0]["tff_match_id"])
    check(len(included) == len(set(included)), "Primary fixture double counted")
    if len(included) == 480:
        check(set(included) == {r["tff_match_id"] for r in primary}, "Recovered season does not cover primary population")
    totals = dict(INCLUDE=10060+len(included), HOLD_OUT=483-len(included), NOT_PLAYED=30, OUT_OF_SCOPE=1)
    check(totals == supplemental["proposed_totals"] == report["proposed_totals"], "Proposed population totals")
    check(sum(totals.values()) == 10574 and frozen["totals"] == supplemental["frozen_registry_totals"],
          "Frozen population changed")
    for name, expected_sha in supplemental["input_sha256"].items():
        check(sha((ROOT/name).read_bytes()) == expected_sha, "Supplement input digest changed")
    return dict(status="PASS", targets=480, primary_fixture_rows=480, primary_originals=60,
                match_detail_originals=len(details), permission_originals=1,
                established=len(included), unresolved=480-len(included), proposed_totals=totals,
                explicit_non_date_repairs=len(repairs), independently_reconciled_club_tables=table_checks,
                method="Independent HTMLParser,original-record binding,directed-pair/score/round checks and duplicate containment;no production recovery imported",
                independence_limit="Shared reviewed season-bound correspondence declarations;TFF primarydates,not two independently sourced exact-date votes per fixture",
                frozen_include_population=10060, original_fields_preserved=True,
                no_round_heading_inference=True, all_results_proposed_only=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    dest = args.directory.resolve()
    check(any(dest.is_relative_to(p.resolve()) for p in
              [PRIVATE, Path(tempfile.gettempdir()), Path("/private/tmp")]), "Private outputs only")
    result = validate(dest)
    raw = enc(result)
    target = dest / "independent_recovery_validation.json"
    if args.verify:
        check(target.read_bytes() == raw, "Independent reconstruction is not reproducible")
    else:
        with target.open("xb") as f:
            f.write(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
