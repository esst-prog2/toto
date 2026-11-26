"""Independent Turkish Phase 4 raw-source-to-CSV reconstruction.

No production standardizer, production source/name parser, shared importer, ID
helper or serializer is imported. Reuses the independent Phase 2 raw grammars
and independent historical decision checks; approved human judgments are shared.
"""
import argparse
from collections import Counter
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import tempfile

from scripts import validate_turkish_super_lig_structure as original_reader
from scripts import verify_turkish_super_lig_decisions as historical
from scripts import verify_turkish_early_dates as early

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/private/turkey/super_lig"
PRIVATE = BASE / "phase4"
OUTPUT = PRIVATE / "validated"
COLUMNS = ("match_id", "date", "league", "season", "home_team", "away_team", "home_goals", "away_goals")
CSV_NAME = "turkish_super_lig_standardized_1992_2026.csv"
EXPECTED = {"INCLUDE": 10540, "HOLD_OUT": 3, "NOT_PLAYED": 30, "OUT_OF_SCOPE": 1}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def enc(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def load(path):
    return json.loads(path.read_bytes())


def check(condition, message):
    if not condition:
        raise ValueError(message)


def reconstruct_originals():
    config = load(BASE / "phase2/config.json")
    recovery_path = ROOT / config["recovery_path"]
    check(sha(recovery_path.read_bytes()) == config["recovery_sha256"], "2006 recovery binding changed")
    rules = {r["source_line"]: r for r in load(recovery_path)["affected_records"]}
    observations = {}
    originals = {}
    for item in config["files"]:
        raw = (ROOT / item["root_path"]).read_bytes()
        check(sha(raw) == item["sha256"] and len(raw) == item["bytes"], "Original source changed")
        originals[item["root_path"]] = item
        if item["kind"].endswith("csv"):
            rows, tables = original_reader.parse_csv(raw, item, rules)
        elif item["kind"] == "txt":
            rows, tables = original_reader.parse_txt(raw, item)
        elif item["kind"] == "rsssf":
            rows, tables = original_reader.parse_rsssf(raw, item)
        else:
            rows = []
        for r in rows:
            check(r["source_id"] not in observations, "Duplicate raw physical observation")
            observations[r["source_id"]] = r
    check(len(observations) == 13894 and len(originals) == 26, "Original source population differs")
    target = load(BASE / "phase2/validated/source_inventory.json")
    check(set(observations) == {r["source_id"] for r in target["observations"]}, "Raw inventory membership differs")
    # Original truth is reconstructed first; the inventory is a comparison target.
    for r in target["observations"]:
        raw_row = observations[r["source_id"]]
        for key in ("source", "source_id", "source_sha256", "physical_sha256", "line", "end_line",
                    "cell", "season", "stage", "date", "home", "away", "hg", "ag", "round", "annotation"):
            check(raw_row[key] == r[key], "Raw source/inventory mismatch: " + key)
        if "original_fields" in raw_row:
            check(raw_row["original_fields"] == r["original_fields"], "Original CSV fields changed")
    check(sum(r["correction"] is not None for r in observations.values()) == 143,
          "143 original date corrections lost")
    return observations, originals


def make_row(season, day, home, away, goals):
    year = int(season[:4])
    check(season == f"{year}/{year+1}" and 1992 <= year <= 2025, "Wrong output season")
    d = date.fromisoformat(day)
    check(day == d.isoformat() and date(year, 7, 1) <= d <=
          (date(2020, 7, 26) if year == 2019 else date(year+1, 6, 30)), "Wrong football date")
    check(all(type(g) is int and g >= 0 for g in goals) and len(goals) == 2, "Wrong final goals")
    check(all(isinstance(v, str) and v == v.strip() and v for v in (home, away)) and home != away,
          "Invalid club labels/orientation")
    identity = ["Turkish Süper Lig", season, day, home, away]
    digest = hashlib.sha256(json.dumps(identity, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    return dict(zip(COLUMNS, (digest, day, identity[0], season, home, away, *goals)))


def csv_bytes(rows):
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(COLUMNS)
    for row in sorted(rows, key=lambda r: tuple(r[k] for k in ("league", "season", "date", "home_team", "away_team"))):
        writer.writerow([row[key] for key in COLUMNS])
    return buffer.getvalue().encode("utf-8")


def check_csv(raw, expected):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""), strict=True)
    check(tuple(reader.fieldnames or ()) == COLUMNS, "Wrong eight-column schema")
    actual = []
    for row in reader:
        check(None not in row and None not in row.values(), "Wrong CSV width")
        for key in ("home_goals", "away_goals"):
            value = row[key]
            check(value.isascii() and value.isdigit() and str(int(value)) == value, "Noncanonical score integer")
            row[key] = int(value)
        check(row == make_row(row["season"], row["date"], row["home_team"], row["away_team"],
                              [row["home_goals"], row["away_goals"]]), "Invalid match ID/league/fields")
        actual.append(row)
    check(len(actual) == len({r["match_id"] for r in actual}) == len(expected), "Missing/extra/duplicate CSV row")
    check(raw == csv_bytes(expected), "Independent full CSV bytes/fields/order differ")
    return actual


def other_dataset_check(ids):
    files = []
    rows = 0
    # Existing standardized datasets only, bounded by this repository root.
    for path in sorted((ROOT / "data/private").rglob("*standardized*.csv")):
        if path.is_relative_to(BASE):
            continue
        raw = path.read_bytes()
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
        check(tuple(reader.fieldnames or ()) == COLUMNS, "Unexpected prior standardized schema")
        for row in reader:
            check(row["league"] != "Turkish Süper Lig" and row["match_id"] not in ids,
                  "Cross-competition league/ID collision")
            rows += 1
        files.append(dict(path=str(path.relative_to(ROOT)), sha256=sha(raw)))
    check(len(files) >= 13, "Prior dataset preservation scope incomplete")
    return dict(files=files, inspected_rows=rows, collisions=0)


def validate(directory=OUTPUT):
    directory = Path(directory)
    observations, originals = reconstruct_originals()
    inventory_rows = {r["source_id"]: r for r in load(BASE / "phase2/validated/source_inventory.json")["observations"]}
    frozen_path = BASE / "phase3/accepted/decision_registry.json"
    supp_path = BASE / "early_date_recovery/proposed/supplemental_decisions.json"
    approval = load(PRIVATE / "approval.json")
    check(approval["frozen_phase3_sha256"] == sha(frozen_path.read_bytes()) and
          approval["supplement_sha256"] == sha(supp_path.read_bytes()) and approval["expected_totals"] == EXPECTED and
          approval["scope"] == "OWNER_APPROVED_480_INCLUDING_NINE_REPAIRS" and approval["phase"] == 4,
          "Missing hash-bound owner approval")
    frozen = load(frozen_path)
    supplemental = load(supp_path)
    check(sha(frozen_path.read_bytes()) == load(BASE / "phase3/execution_manifest.json")["artifacts"]["decision_registry.json"],
          "Frozen Phase 3 changed")
    check(sha(supp_path.read_bytes()) == load(BASE / "early_date_recovery/execution_manifest.json")["artifacts"]["supplemental_decisions.json"],
          "Approved supplement changed")
    # Existing independent checker reconstructs the complete TFF/RSSSF recovery,
    # including all nine bound repairs and 32 independent final-table checks.
    early_assessment = early.validate()
    check(early_assessment["established"] == 480 and early_assessment["explicit_non_date_repairs"] == 9,
          "Approved recovery evidence no longer validates")
    rounds = {}
    for item in load(BASE / "early_date_recovery/fixture_plan.json")["items"]:
        raw = (BASE / "early_date_recovery" / item["path"]).read_bytes()
        for fixture in early.parse(raw, item):
            check(fixture["tff_match_id"] not in rounds, "Duplicate TFF fixture")
            rounds[fixture["tff_match_id"]] = fixture
    overlap = load(BASE / "phase2/validated/overlap_assessment.json")
    events = {e["event_id"]: e for e in overlap["conditional_events"]}
    frozen_byid = {d["event_id"]: d for d in frozen["decisions"]}
    additions = {d["event_id"]: d for d in supplemental["decisions"]}
    check(len(events) == len(frozen_byid) == 10574 and len(additions) == 480, "Population differs")
    cases = load(BASE / "phase3/case_rules.v2.json")
    evidence = load(BASE / "phase3/evidence_index.v2.json")["entries"]
    check(sha((BASE / "phase3/case_rules.v2.json").read_bytes()) == frozen["case_rules_sha256"] and
          sha((BASE / "phase3/evidence_index.v2.json").read_bytes()) == frozen["evidence_index_sha256"],
          "Approved historical evidence changed")
    registry = load(directory / "approved_decision_registry.json")
    check(registry["approval"] == approval and registry["policy"] == frozen["policy"] and
          registry["policy_version"] == frozen["policy_version"], "Retrospective policy drift")
    composed = {d["event_id"]: d for d in registry["decisions"]}
    check(len(registry["decisions"]) == len(composed) == 10574 and set(composed) == set(events), "Composed event population differs")
    expected_rows = []
    byevent = {}
    dispositions = Counter()
    for eid, event in events.items():
        old = frozen_byid[eid]
        members = [observations[sid] for sid in event["source_ids"]]
        historical.check_decision(event, members, old, cases["cases"].get(eid), evidence)
        d = composed[eid]
        expected_fields = dict(old, frozen_decision_sha256=sha(enc(old)), approval_basis="APPROVED_PHASE3")
        addition = additions.get(eid)
        if addition:
            check(old["disposition"] == "HOLD_OUT" and old["accepted"] is None and len(members) == 1,
                  "Supplement restored wrong excluded event")
            proposed = addition["candidate_fixtures"][0]
            fixture = rounds[proposed["tff_match_id"]]
            check(fixture == proposed and fixture["season"] == old["season"] and
                  fixture["stage"] == old["source_stage"] == "REGULAR_SEASON", "Raw TFF fixture identity differs")
            chosen = dict(original_football_date=fixture["date"], completion_date=None,
                          final_score=fixture["score"], identity_source_id=old["source_ids"][0],
                          date_source_ids=[], score_source_ids=[])
            expected_fields.update(disposition="INCLUDE", reason=addition["reason"],
                approval_basis="OWNER_APPROVED_EARLY_DATE_SUPPLEMENT", approved_supplement=addition, accepted=chosen)
            output = make_row(old["season"], fixture["date"], fixture["home"], fixture["away"], fixture["score"])
        elif old["disposition"] == "INCLUDE":
            rule = cases["cases"].get(eid)
            anchor = observations[event["anchor"]]
            if rule:
                fact = rule["fact_assertion"]
                day, goals = fact["original_football_date"], fact["accepted_final_score"]
            else:
                days = {r["date"] for r in members if r["date"] and r["hg"] is not None}
                scores = {(int(r["hg"]), int(r["ag"])) for r in members if r["hg"] is not None}
                check(len(days) == len(scores) == 1, "Unreviewed raw date/result conflict")
                day, goals = next(iter(days)), list(next(iter(scores)))
            output = make_row(old["season"], day, anchor["home"], anchor["away"], goals)
        else:
            output = None
        check(d == expected_fields, "Composed decision changed an unapproved field")
        dispositions[d["disposition"]] += 1
        byevent[eid] = output
        if output:
            expected_rows.append(output)
    check(dict(dispositions) == registry["totals"] == EXPECTED and len(expected_rows) == 10540,
          "Final disposition/row totals differ")
    check(Counter(s for d in composed.values() for s in d["source_ids"]) == Counter(observations.keys()),
          "Source overlap lost or double counted")
    raw_csv = (directory / CSV_NAME).read_bytes()
    rows = check_csv(raw_csv, expected_rows)
    rowindex = {r["match_id"]: (n, r) for n, r in enumerate(rows, 2)}
    audit = load(directory / "source_to_output_audit.json")
    check(len(audit["events"]) == len({r["event_id"] for r in audit["events"]}) == 10574,
          "Audit population incomplete")
    for a in audit["events"]:
        eid = a["event_id"]
        output = byevent[eid]
        check(a["output"] == output and a["disposition"] == composed[eid]["disposition"] and
              a["decision_sha256"] == sha(enc(composed[eid])) and
              a["supplemental_evidence"] == additions.get(eid), "Audit output/decision mismatch")
        check(a["csv_physical_row"] == (rowindex[output["match_id"]][0] if output else None), "CSV physical row trace differs")
        check([c["source_id"] for c in a["contributors"]] == events[eid]["source_ids"], "Audit contributor membership differs")
        for c in a["contributors"]:
            r = observations[c["source_id"]]
            for key in ("source", "source_sha256", "physical_sha256", "line", "end_line", "cell"):
                check(c[key] == r[key], "Physical source trace mismatch")
            check(c["source_url"] == originals[r["source"]]["url"], "Source URL trace mismatch")
            check(c["observation_sha256"] == sha(enc(inventory_rows[c["source_id"]])), "Observation audit binding differs")
    matrix = load(directory / "season_stage_coverage.json")
    before = load(BASE / "phase3/accepted/season_stage_decisions.json")["coverage"]
    check(len(matrix["coverage"]) == 36 and [r["season"] for r in matrix["coverage"]] == [r["season"] for r in before],
          "Coverage matrix incomplete")
    for record, prior in zip(matrix["coverage"], before):
        season = record["season"]
        selected = [d for d in composed.values() if d["season"] == season]
        canonical = [r for r in rows if r["season"] == season]
        stages = {}
        for d in selected:
            stages.setdefault(d["source_stage"], Counter())[d["disposition"]] += 1
        check(record == dict(season=season, conditional_events=len(selected),
            dispositions={k: sum(d["disposition"] == k for d in selected) for k in EXPECTED},
            stages={k: dict(v) for k, v in stages.items()}, rows=len(canonical),
            clubs=len({r[k] for r in canonical for k in ("home_team", "away_team")}),
            first_date=min((r["date"] for r in canonical), default=None),
            last_date=max((r["date"] for r in canonical), default=None), exact_date_gap=not canonical,
            source_gap_slots=prior["source_gap_slots"], nominal_regular_slots=prior["nominal_regular_slots"]),
            "Season/stage/date/identity coverage differs")
    check(matrix["missing_eligible_postseason_2011_2012"] == 24 and matrix["absent_regular_slots_2009_2010"] == 34,
          "Known coverage gaps hidden")
    manifest = load(directory / "standardization_manifest.json")
    for name, digest in manifest["artifacts"].items():
        check(sha((directory / name).read_bytes()) == digest, "Artifact hash differs")
    for path, digest in registry["input_sha256"].items():
        check(sha((ROOT / path).read_bytes()) == digest, "Bound input changed")
    prior = other_dataset_check({r["match_id"] for r in rows})
    return dict(status="PASS", rows=10540, unique_ids=len(rowindex), conditional_events=10574,
        totals=EXPECTED, source_observations=len(observations), original_sources=26,
        supplemental_originals=70, recovered=480, approved_repairs=9, supported_2006_date_corrections=143,
        retained_hold_out=3, excluded_without_output=34, csv_sha256=sha(raw_csv), independent_bytes_equal=True,
        seasons=dict(sorted(Counter(r["season"] for r in rows).items())), stages={"REGULAR_SEASON":10540},
        prior_standardized=prior, evidence_independence=early_assessment["independence_limit"],
        method="Independent original grammars,approved historical fact checks,independent TFF HTMLParser,club labels,all eight fields,SHA256 identity,ordering and CSV serialization;no production standardization helpers"), csv_bytes(expected_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=OUTPUT)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--reconstructed-csv", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    report, reconstructed = validate(args.directory)
    targets = [(args.report or args.directory / "independent_standardization_validation.json", enc(report))]
    if args.reconstructed_csv:
        targets.append((args.reconstructed_csv, reconstructed))
    for path, raw in targets:
        path = path.resolve()
        check(path.is_relative_to(PRIVATE.resolve()) or path.is_relative_to(Path(tempfile.gettempdir()).resolve()),
              "Independent output must remain private or temporary")
        if args.verify:
            check(path.read_bytes() == raw, "Independent reproduction differs")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as f:
                f.write(raw)
    print(json.dumps({k:report[k] for k in ["status", "rows", "unique_ids", "totals", "csv_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
