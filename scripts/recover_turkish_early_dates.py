"""Propose Turkish early-date supplements without altering frozen decisions.

Only explicit, newly preserved fixture dates can qualify. Round headings are
documentary context, never date inference. Exact season-bound identity, directed
pair, score, one-to-one correspondence and prior HOLD OUT are required.
"""
from collections import Counter, defaultdict
from datetime import date, datetime
from html import unescape
from pathlib import Path
import argparse
import json
import re
import tempfile
from urllib.parse import parse_qs, urlsplit

from scripts import collect_turkish_super_lig_sources as acquisition

ROOT = acquisition.ROOT
PRIVATE = ROOT / "data/private/turkey/super_lig/early_date_recovery"
OUTPUT = PRIVATE / "proposed"
PHASE2 = PRIVATE.parent / "phase2/validated"
PHASE3 = PRIVATE.parent / "phase3/accepted"
NAMES = ("affected_events.json", "supplemental_decisions.json", "recovery_assessment.json")


def load(path):
    return json.loads(path.read_bytes())


def plain(raw):
    return " ".join(unescape(re.sub(r"<[^>]*>", " ", raw)).split())


def parse_tff(raw, item, receipt):
    text = raw.decode("iso-8859-9")
    year = int(item["season"][:4])
    expected_page = {"1992/1993": "560", "1993/1994": "559"}.get(item["season"])
    query = {k.lower(): v for k, v in parse_qs(urlsplit(item["url"]).query).items()}
    if not expected_page or query.get("pageid") != [expected_page]:
        raise ValueError("Not an allowlisted top-division archive page")
    if f"{year}-{year+1} Sezonu" not in text:
        raise ValueError("TFF season title mismatch")
    markers = re.findall(r">(\d+)\.Hafta<", text)
    if markers != [str(item["round"])]:
        raise ValueError("TFF round selection mismatch")
    rows = []
    pattern = rb'<tr class="haftaninMaclariTr">.*?</tr>'
    for match in re.finditer(pattern, raw, re.S):
        snippet = match.group().decode("iso-8859-9")
        cells = dict(re.findall(r'<td[^>]*class="(haftaninMaclari\w+)"[^>]*>(.*?)</td>',
                                snippet, re.S))
        if set(cells) != {"haftaninMaclariTarih", "haftaninMaclariEv",
                          "haftaninMaclariSkor", "haftaninMaclariDeplasman",
                          "haftaninMaclariDetay"}:
            raise ValueError("TFF fixture cell schema")
        dates = re.findall(r'lblTarih">([^<]+)</span>', cells["haftaninMaclariTarih"])
        if len(dates) != 1:
            raise ValueError("Missing explicit fixture date")
        day = datetime.strptime(dates[0], "%d.%m.%Y").date()
        if not date(year, 7, 1) <= day <= date(year+1, 6, 30):
            raise ValueError("TFF fixture outside season")
        score = re.fullmatch(r"(\d+)\s*-\s*(\d+)", plain(cells["haftaninMaclariSkor"]))
        ids = set(re.findall(r"macId=(\d+)", snippet, re.I))
        if not score or len(ids) != 1:
            raise ValueError("TFF fixture score or identity invalid")
        start, end = match.span()
        first = raw[:start].count(b"\n") + 1
        last = first + match.group().count(b"\n")
        rows.append(dict(season=item["season"], stage="REGULAR_SEASON", round=item["round"],
                         date=day.isoformat(), home=plain(cells["haftaninMaclariEv"]),
                         away=plain(cells["haftaninMaclariDeplasman"]),
                         score=[int(score[1]), int(score[2])], tff_match_id=next(iter(ids)),
                         source=str((PRIVATE / item["path"]).relative_to(ROOT)),
                         source_sha256=receipt["sha256"], source_url=item["url"],
                         line=first, end_line=last, byte_start=start, byte_end=end,
                         record_sha256=acquisition.sha(match.group())))
    if len(rows) != 8 or len({r["tff_match_id"] for r in rows}) != 8:
        raise ValueError("Expected eight distinct target fixtures per TFF round")
    return rows


def parse_match_detail(raw):
    """Only the official professional match panel, never youth/name-only hits."""
    text = raw.decode("iso-8859-9")
    fields = {}
    for suffix in ("lnkTakim1", "lnkTakim2", "lblTakim1Skor", "Label12",
                   "lblTarih", "lblOrganizasyonAdi"):
        pattern = (r'<(?:a|span)\b[^>]*id="[^"]*_MacBilgiDisplay1_dtMacBilgisi_' +
                   re.escape(suffix) + r'"[^>]*>(.*?)</(?:a|span)>')
        found = re.findall(pattern, text, re.S)
        if len(found) != 1:
            raise ValueError("Missing or ambiguous official match field: " + suffix)
        fields[suffix] = plain(found[0])
    if "Profesyonel Takım" not in fields["lblOrganizasyonAdi"] or "Lig" not in fields["lblOrganizasyonAdi"]:
        raise ValueError("Official detail is not a professional league fixture")
    day = datetime.strptime(fields["lblTarih"].split(" - ")[0], "%d.%m.%Y").date().isoformat()
    if not all(fields[k].isdigit() for k in ("lblTakim1Skor", "Label12")):
        raise ValueError("Official match detail lacks a numeric final score")
    return dict(date=day, home=fields["lnkTakim1"], away=fields["lnkTakim2"],
                score=[int(fields["lblTakim1Skor"]), int(fields["Label12"])],
                competition=fields["lblOrganizasyonAdi"])


def extract_targets(inventory, registry):
    observations = {r["source_id"]: r for r in inventory["observations"]}
    targets, other_holds = [], []
    for decision in registry["decisions"]:
        if decision["disposition"] != "HOLD_OUT":
            continue
        if decision["season"] not in {"1992/1993", "1993/1994"}:
            other_holds.append(decision["event_id"])
            continue
        if len(decision["source_ids"]) != 1:
            raise ValueError("Early target membership expanded")
        row = observations[decision["source_ids"][0]]
        if row["date"] is not None or row["hg"] is None:
            raise ValueError("Target is not a scored uncertified-date record")
        targets.append(dict(event_id=decision["event_id"], frozen_decision=decision,
                            source_observation=row,
                            available_date_information=row.get("nominal_date_heading"),
                            insufficient_reason="Round heading lacks fixture-specific day certification" if row["round"]
                            else "Result grid contains no fixture dates"))
    if len(targets) != 480 or Counter(t["source_observation"]["season"] for t in targets) != {
            "1992/1993": 240, "1993/1994": 240} or len(other_holds) != 3:
        raise ValueError("Frozen supplemental target population changed")
    return targets, sorted(other_holds)


def assess_target(target, fixtures, mapping):
    original = target["source_observation"]
    home, away = mapping.get(original["home"]), mapping.get(original["away"])
    if home is None or away is None:
        return dict(proposed_disposition="HOLD_OUT", reason="UNRESOLVED_SOURCE_IDENTITY",
                    candidate_fixtures=[], proposed_date=None)
    candidates = [r for r in fixtures if r["season"] == original["season"] and
                  r["stage"] == original["stage"] and (r["home"], r["away"]) == (home, away)]
    if len(candidates) != 1:
        return dict(proposed_disposition="HOLD_OUT", reason="MISSING_OR_AMBIGUOUS_DIRECTED_FIXTURE",
                    candidate_fixtures=candidates, proposed_date=None)
    candidate = candidates[0]
    if candidate["score"] != [int(original["hg"]), int(original["ag"])]:
        return dict(proposed_disposition="HOLD_OUT", reason="SOURCE_SCORE_CONFLICT",
                    candidate_fixtures=candidates, proposed_date=None)
    if original["round"] and candidate["round"] != original["round"]:
        return dict(proposed_disposition="HOLD_OUT", reason="SOURCE_ROUND_IDENTITY_CONFLICT",
                    candidate_fixtures=candidates, proposed_date=None)
    return dict(proposed_disposition="INCLUDE", reason="PRIMARY_EXPLICIT_DATE_EXACT_FIXTURE_CORRESPONDENCE",
                candidate_fixtures=candidates, proposed_date=candidate["date"])


def validate_repair(original, repair, candidate, detail, mapping):
    if (acquisition.sha(acquisition.encode(original)) != repair["source_observation_sha256"] or
            original["source_id"] != repair["source_id"]):
        raise ValueError("Source-specific repair binding failed")
    if any(detail[k] != candidate[k] or candidate[k] != repair["proposed_fields"][k]
           for k in ("date", "home", "away", "score")):
        raise ValueError("Official match detail does not support source repair")
    if candidate["season"] != original["season"] or (
            original["round"] and candidate["round"] != original["round"]):
        raise ValueError("Repair changes source season/round")
    h, a = (mapping.get(original[k]) for k in ("home", "away"))
    old_score = [int(original["hg"]), int(original["ag"])]
    kind = repair["repair_kind"]
    if kind == "SCORE_CORRECTION":
        valid = (h, a) == (candidate["home"], candidate["away"]) and old_score != candidate["score"]
    elif kind == "OPPONENT_CORRECTION":
        valid = h == candidate["home"] and a is not None and a != candidate["away"] and old_score == candidate["score"]
    elif kind == "SOURCE_LABEL_CORRECTION":
        valid = h == candidate["home"] and a is None and old_score == candidate["score"]
    else:
        valid = False
    if not valid:
        raise ValueError("Repair exceeds its reviewed field-change scope")


def build():
    inventory = load(PHASE2 / "source_inventory.json")
    registry = load(PHASE3 / "decision_registry.json")
    expected = load(PRIVATE.parent / "phase3/execution_manifest.json")["artifacts"]
    if acquisition.sha((PHASE3 / "decision_registry.json").read_bytes()) != expected["decision_registry.json"]:
        raise ValueError("Frozen Phase 3 registry changed")
    targets, other_holds = extract_targets(inventory, registry)
    fixtures = []
    plan = acquisition.validate_plan(load(PRIVATE / "fixture_plan.json"))
    receipts = []
    for item in plan["items"]:
        receipt = load(PRIVATE / (item["path"] + ".provenance.json"))
        raw = acquisition.verify(PRIVATE, item, receipt)
        fixtures.extend(parse_tff(raw, item, receipt))
        receipts.append(dict(path=item["path"], sha256=receipt["sha256"], bytes=receipt["bytes"],
                             url=item["url"], retrieved_at_utc=receipt["retrieved_at_utc"]))
    if len(fixtures) != 480 or len({r["tff_match_id"] for r in fixtures}) != 480:
        raise ValueError("Supplementary primary fixture population incomplete or duplicated")
    config = load(PRIVATE / "identity_config.json")
    repairs = load(PRIVATE / "repair_rules.json")
    details = {}
    for item in acquisition.validate_plan(load(PRIVATE / "case_evidence_plan.json"))["items"]:
        receipt = load(PRIVATE / (item["path"] + ".provenance.json"))
        raw = acquisition.verify(PRIVATE, item, receipt)
        details[item["tff_match_id"]] = dict(parse_match_detail(raw),
            source=str((PRIVATE/item["path"]).relative_to(ROOT)),
            source_sha256=receipt["sha256"], url=item["url"],
            retrieved_at_utc=receipt["retrieved_at_utc"])
    byseason = defaultdict(list)
    for row in fixtures:
        byseason[row["season"]].append(row)
    decisions = []
    for target in targets:
        season = target["source_observation"]["season"]
        proposal = assess_target(target, byseason[season], config["source_season_maps"][season])
        repair = repairs["cases"].get(target["event_id"])
        if repair:
            original = target["source_observation"]
            candidate = [r for r in byseason[season] if r["tff_match_id"] == repair["tff_match_id"]]
            if len(candidate) != 1:
                raise ValueError("Repair primary fixture absent or ambiguous")
            candidate = candidate[0]
            detail = details[repair["tff_match_id"]]
            validate_repair(original, repair, candidate, detail, config["source_season_maps"][season])
            proposal = dict(proposed_disposition="INCLUDE", reason="REVIEWED_SOURCE_SPECIFIC_REPAIR",
                            proposed_date=candidate["date"], candidate_fixtures=[candidate],
                            source_repair=repair, official_match_detail=detail)
        decisions.append(dict(event_id=target["event_id"], season=season,
                              old_disposition="HOLD_OUT", old_accepted=None,
                              source_ids=target["frozen_decision"]["source_ids"],
                              source_observation_sha256=acquisition.sha(acquisition.encode(target["source_observation"])),
                              approval_state="PROPOSED_ONLY", **proposal))
    # A source defect must not create two accepted events for one actual fixture.
    reverse = defaultdict(list)
    for decision in decisions:
        if decision["proposed_disposition"] == "INCLUDE":
            reverse[decision["candidate_fixtures"][0]["tff_match_id"]].append(decision)
    for group in reverse.values():
        if len(group) > 1:
            for decision in group:
                decision.update(proposed_disposition="HOLD_OUT", proposed_date=None,
                                reason="MULTIPLE_FROZEN_EVENTS_FOR_ONE_PRIMARY_FIXTURE")
    decisions.sort(key=lambda d: d["event_id"])
    recovered = sum(d["proposed_disposition"] == "INCLUDE" for d in decisions)
    totals = dict(INCLUDE=10060+recovered, HOLD_OUT=483-recovered, NOT_PLAYED=30, OUT_OF_SCOPE=1)
    summary = []
    for season in ["1992/1993", "1993/1994"]:
        subset = [d for d in decisions if d["season"] == season]
        summary.append(dict(season=season, targets=len(subset),
                            proposed_recovered=sum(d["proposed_disposition"] == "INCLUDE" for d in subset),
                            reasons=dict(sorted(Counter(d["reason"] for d in subset).items()))))
    inputs = {str(p.relative_to(ROOT)): acquisition.sha(p.read_bytes()) for p in
              [PHASE2 / "source_inventory.json", PHASE3 / "decision_registry.json",
               PRIVATE / "identity_config.json", PRIVATE / "fixture_plan.json",
               PRIVATE / "permission_assessment.json", PRIVATE / "repair_rules.json",
               PRIVATE / "case_evidence_plan.json", PRIVATE / "existing_source_review.json",
               PRIVATE / "aggregate_identity_config.json", PRIVATE / "research_register.json"]}
    distributions = []
    for season in ("1992/1993", "1993/1994"):
        original_rows = [t["source_observation"] for t in targets if t["source_observation"]["season"] == season]
        dates = Counter("NO_DATE" if not r.get("nominal_date_heading") else
                        "ROUND_RANGE" if "-" in r["nominal_date_heading"] else
                        "SINGLE_DAY_NOMINAL_HEADING" for r in original_rows)
        distributions.append(dict(season=season, source=original_rows[0]["source"],
            source_sha256=original_rows[0]["source_sha256"], events=len(original_rows),
            date_information=dict(sorted(dates.items())),
            nominal_heading_counts=dict(sorted(Counter(r.get("nominal_date_heading") or "NONE" for r in original_rows).items())),
            raw_team_participations=dict(sorted(Counter(r[k] for r in original_rows for k in ("home", "away")).items())),
            reported_score_counts=dict(sorted(Counter(r["hg"]+"-"+r["ag"] for r in original_rows).items()))))
    return dict(zip(NAMES, [dict(population=480, events=targets, untouched_other_hold_event_ids=other_holds,
                                distributions=distributions,
                                four_exact_date_gap_seasons=["1990/1991", "1991/1992", "1992/1993", "1993/1994"],
                                seasons_without_fixture_descriptions=["1990/1991", "1991/1992"]),
                           dict(status="PROPOSED_PENDING_OWNER_APPROVAL", input_sha256=inputs,
                                frozen_registry_totals=registry["totals"], proposed_totals=totals,
                                decisions=decisions, original_receipts=receipts,
                                boundary="No changes to frozen registry or approved INCLUDE population;no standardized data",
                                independence="TFF governing-body fixture records separately corroborate frozen RSSSF identities/scores;no assertion of disjoint upstreams or two independent exact-date providers"),
                           dict(targets=480, established=recovered, unresolved=480-recovered,
                                season_summary=summary, proposed_totals=totals,
                                supplementary_fixture_originals=len(receipts),
                                additional_match_detail_originals=len(details),
                                non_date_repairs=len(repairs["cases"]),
                                source_bytes=sum(r["bytes"] for r in receipts),
                                secondary_search_is_not_a_source_vote=True,
                                date_rule="Explicit date inside exact directed fixture row;never round-heading inference")]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    dest = args.output.resolve()
    if not any(dest.is_relative_to(p.resolve()) for p in
               (PRIVATE, Path(tempfile.gettempdir()), Path("/private/tmp"))):
        raise ValueError("Private or temporary output required")
    artifacts = build()
    if not args.verify and any((dest / name).exists() for name in NAMES):
        raise FileExistsError("Supplemental proposals already frozen")
    for name, value in artifacts.items():
        raw = acquisition.encode(value)
        if args.verify:
            if (dest / name).read_bytes() != raw:
                raise ValueError("Supplement is not reproducible")
        else:
            acquisition.save(dest / name, raw)
    print(json.dumps(artifacts["recovery_assessment.json"], sort_keys=True))


if __name__ == "__main__":
    main()
