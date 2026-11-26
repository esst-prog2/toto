"""Offline Turkish Phase 4 projection of owner-approved, frozen decisions.

No acquisition, historical adjudication, application integration or publication.
The original registries remain immutable inputs; the composed registry is new.
"""
import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import tempfile

from scripts.artifact_io import check_overwrite, serialize_csv
from scripts import recover_turkish_early_dates as recovery
from toto_estimator.historical_import import (
    OUTPUT_COLUMNS, HistoricalSource, import_historical_csvs,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/private/turkey/super_lig"
PRIVATE = BASE / "phase4"
OUTPUT = PRIVATE / "validated"
LEAGUE = "Turkish Süper Lig"
CSV_NAME = "turkish_super_lig_standardized_1992_2026.csv"
EXPECTED = dict(INCLUDE=10540, HOLD_OUT=3, NOT_PLAYED=30, OUT_OF_SCOPE=1)
NAMES = ("approved_decision_registry.json", CSV_NAME, "source_to_output_audit.json",
         "season_stage_coverage.json", "standardization_manifest.json")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def load(path):
    return json.loads(path.read_bytes())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bind_inputs():
    """Check approved manifest chains and reproduce the frozen supplement."""
    inputs = {}
    for scope, directory in [(BASE / "phase3", BASE / "phase3/accepted"),
                             (BASE / "early_date_recovery", BASE / "early_date_recovery/proposed")]:
        for name, digest in load(scope / "execution_manifest.json")["artifacts"].items():
            path = directory / name
            require(sha(path.read_bytes()) == digest, "Frozen artifact changed: " + name)
            inputs[str(path.relative_to(ROOT))] = digest
    for name, value in recovery.build().items():
        path = BASE / "early_date_recovery/proposed" / name
        require(path.read_bytes() == encode(value), "Approved supplement does not reproduce: " + name)
    for name in ["source_inventory.json", "overlap_assessment.json", "season_stage_coverage.json",
                 "discrepancy_registry.json", "structural_checks.json"]:
        path = BASE / "phase2/validated" / name
        expected = load(BASE / "phase2/final_status.json")["artifacts"][name]
        require(sha(path.read_bytes()) == expected, "Frozen inventory changed")
        inputs[str(path.relative_to(ROOT))] = expected
    path = PRIVATE / "approval.json"
    inputs[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return inputs


def compose(frozen, supplement, observations, approval):
    """A new derived view; the frozen records and proposals are never edited."""
    require(approval["phase"] == 4 and approval["scope"] == "OWNER_APPROVED_480_INCLUDING_NINE_REPAIRS",
            "Missing explicit Phase 4/supplement approval")
    require(approval["expected_totals"] == EXPECTED, "Approval totals differ")
    overrides = {d["event_id"]: d for d in supplement["decisions"]}
    require(len(overrides) == len(supplement["decisions"]) == 480, "Supplement population changed")
    decisions = []
    for old in frozen["decisions"]:
        d = deepcopy(old)
        d["frozen_decision_sha256"] = sha(encode(old))
        d["approval_basis"] = "APPROVED_PHASE3"
        addition = overrides.get(old["event_id"])
        if addition:
            require(old["disposition"] == "HOLD_OUT" and old["accepted"] is None and
                    old["season"] in ("1992/1993", "1993/1994"), "Supplement exceeds frozen scope")
            require(addition["old_disposition"] == "HOLD_OUT" and addition["old_accepted"] is None and
                    addition["source_ids"] == old["source_ids"] and
                    addition["season"] == old["season"], "Supplement event binding differs")
            require(len(old["source_ids"]) == 1 and addition["source_observation_sha256"] ==
                    sha(encode(observations[old["source_ids"][0]])), "Supplement source binding differs")
            require(addition["proposed_disposition"] == "INCLUDE" and
                    len(addition["candidate_fixtures"]) == 1, "Unapproved supplemental result")
            candidate = addition["candidate_fixtures"][0]
            require(candidate["season"] == old["season"] and
                    candidate["stage"] == old["source_stage"] == "REGULAR_SEASON" and
                    addition["proposed_date"] == candidate["date"], "Supplement season/stage/date differs")
            d.update(disposition="INCLUDE", reason=addition["reason"],
                     approval_basis="OWNER_APPROVED_EARLY_DATE_SUPPLEMENT",
                     approved_supplement=deepcopy(addition),
                     accepted=dict(original_football_date=candidate["date"],
                         completion_date=None, final_score=candidate["score"],
                         identity_source_id=old["source_ids"][0],
                         date_source_ids=[], score_source_ids=[]))
            # These IDs refer to the original inventory; TFF evidence has its
            # separate exact URL/hash/physical locator in approved_supplement.
        decisions.append(d)
    require(set(overrides) <= {d["event_id"] for d in decisions}, "Orphan supplement")
    require(len(decisions) == len({d["event_id"] for d in decisions}) == 10574,
            "Conditional population changed")
    require(dict(Counter(d["disposition"] for d in decisions)) == EXPECTED, "Final dispositions differ")
    require(sum("source_repair" in d.get("approved_supplement", {}) for d in decisions) == 9,
            "Approved nine-repair scope changed")
    return sorted(decisions, key=lambda d: d["event_id"])


def project(decision, observations):
    if decision["disposition"] != "INCLUDE":
        require(decision["accepted"] is None, "Excluded values would leak into CSV")
        return None
    accepted = decision["accepted"]
    season = decision["season"]
    year = int(season[:4])
    require(season == f"{year}/{year+1}" and 1992 <= year <= 2025, "Unapproved season")
    require(decision["source_stage"] == "REGULAR_SEASON", "Unapproved included stage")
    if "approved_supplement" in decision:
        fixture = decision["approved_supplement"]["candidate_fixtures"][0]
        home, away = fixture["home"], fixture["away"]
    else:
        anchor = observations[accepted["identity_source_id"]]
        require(anchor["source_id"] in decision["source_ids"] and anchor["season"] == season and
                anchor["stage"] == decision["source_stage"], "Unsupported identity anchor")
        home, away = anchor["home"], anchor["away"]
    require(all(isinstance(s, str) and s and s == s.strip() for s in (home, away)) and home != away,
            "Invalid source-supported opponents")
    day = date.fromisoformat(accepted["original_football_date"])
    end = date(2020, 7, 26) if year == 2019 else date(year+1, 6, 30)
    require(date(year, 7, 1) <= day <= end, "Football date outside approved season window")
    score = accepted["final_score"]
    require(len(score) == 2 and all(type(g) is int and g >= 0 for g in score), "Invalid accepted goals")
    return dict(date=day.isoformat(), league=LEAGUE, season=season,
                home_team=home, away_team=away, home_goals=score[0], away_goals=score[1])


def convert(projections):
    identities = [tuple(r[k] for k in ("league", "season", "date", "home_team", "away_team"))
                  for r in projections]
    require(len(identities) == len(set(identities)), "Approved events collide under shared identity")
    bridge = []
    for r in projections:
        day = date.fromisoformat(r["date"])
        h, a = r["home_goals"], r["away_goals"]
        bridge.append(dict(Date=day.strftime("%d/%m/%Y"), Season=r["season"],
            HomeTeam=r["home_team"], AwayTeam=r["away_team"], FTHG=h, FTAG=a,
            FTR="H" if h > a else "A" if h < a else "D"))
    with tempfile.TemporaryDirectory(prefix="turkey-phase4-bridge-") as temp:
        path = Path(temp) / "bridge.csv"
        path.write_bytes(serialize_csv(bridge, ("Date", "Season", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR")))
        imported = import_historical_csvs([HistoricalSource(path, LEAGUE)])
    require(not imported.issues and imported.summary == dict(total=len(bridge), accepted=len(bridge),
            rejected=0, duplicates=0, fixtures=0, conflicts=0), "Shared importer changed/rejected approved events")
    actual = [{k: r[k] for k in projections[0]} for r in imported.records] if projections else []
    require(Counter(encode(r) for r in actual) == Counter(encode(r) for r in projections),
            "Shared importer changed approved fields")
    return serialize_csv(imported.records, OUTPUT_COLUMNS), imported.records, imported.summary


def coverage(decisions, rows):
    result = []
    before = load(BASE / "phase3/accepted/season_stage_decisions.json")["coverage"]
    for original in before:
        season = original["season"]
        subset = [d for d in decisions if d["season"] == season]
        standardized = [r for r in rows if r["season"] == season]
        stages = {}
        for d in subset:
            stages.setdefault(d["source_stage"], Counter())[d["disposition"]] += 1
        result.append(dict(season=season, conditional_events=len(subset),
            dispositions={key: sum(d["disposition"] == key for d in subset) for key in EXPECTED},
            stages={k: dict(v) for k, v in sorted(stages.items())}, rows=len(standardized),
            clubs=len({r[k] for r in standardized for k in ("home_team", "away_team")}),
            first_date=min((r["date"] for r in standardized), default=None),
            last_date=max((r["date"] for r in standardized), default=None),
            exact_date_gap=not standardized, source_gap_slots=original["source_gap_slots"],
            nominal_regular_slots=original["nominal_regular_slots"]))
    return dict(coverage=result, missing_eligible_postseason_2011_2012=24,
                absent_regular_slots_2009_2010=34, absent_fixtures_are_not_not_played=True)


def build():
    inputs = bind_inputs()
    frozen = load(BASE / "phase3/accepted/decision_registry.json")
    supplement = load(BASE / "early_date_recovery/proposed/supplemental_decisions.json")
    approval = load(PRIVATE / "approval.json")
    require(approval["frozen_phase3_sha256"] == sha(encode(frozen)) and
            approval["supplement_sha256"] == sha(encode(supplement)), "Approval digest differs")
    inventory = load(BASE / "phase2/validated/source_inventory.json")
    observations = {r["source_id"]: r for r in inventory["observations"]}
    decisions = compose(frozen, supplement, observations, approval)
    projections = [(d, project(d, observations)) for d in decisions]
    raw, rows, summary = convert([r for d, r in projections if r is not None])
    require(len(rows) == len({r["match_id"] for r in rows}) == 10540, "Wrong canonical population")
    index = {tuple(r[k] for k in ("league", "season", "date", "home_team", "away_team")): (n, r)
             for n, r in enumerate(rows, 2)}
    catalogue = {r["root_path"]: r for r in inventory["catalogue"]}
    audit = []
    for d, projection in projections:
        selected = index.get(tuple(projection[k] for k in ("league", "season", "date", "home_team", "away_team"))) if projection else None
        contributors = []
        for sid in d["source_ids"]:
            r = observations[sid]
            contributors.append(dict(source_id=sid, source=r["source"], source_url=catalogue[r["source"]]["url"],
                source_sha256=r["source_sha256"], line=r["line"], end_line=r["end_line"],
                cell=r["cell"], physical_sha256=r["physical_sha256"],
                observation_sha256=sha(encode(r))))
        audit.append(dict(event_id=d["event_id"], disposition=d["disposition"],
            decision_sha256=sha(encode(d)), contributors=contributors,
            csv_physical_row=selected[0] if selected else None, output=selected[1] if selected else None,
            supplemental_evidence=d.get("approved_supplement"),
            inventory_reference="Frozen source_inventory.json retains every original field and correction",
            decision_reference="approved_decision_registry.json retains historical evidence and completion dates"))
    registry = dict(phase=4, approval=approval, policy=frozen["policy"], policy_version=frozen["policy_version"],
        input_sha256=inputs, totals=EXPECTED, decisions=decisions,
        original_sha256=frozen["original_sha256"], frozen_records_unchanged=True)
    artifacts = {NAMES[0]: encode(registry), CSV_NAME: raw,
        NAMES[2]: encode(dict(events=audit, conditional_events=10574, source_observations=13894,
                             input_sha256=inputs)), NAMES[3]: encode(coverage(decisions, rows))}
    artifacts[NAMES[4]] = encode(dict(phase=4, league=LEAGUE, rows=len(rows), totals=EXPECTED,
        input_sha256=inputs, artifacts={k: sha(v) for k, v in artifacts.items()}, importer_summary=summary,
        naming="TFF explicit professional labels for recovered 1992/93-1993/94;otherwise frozen identity anchor labels;whitespace-only shared normalization;no global aliases",
        serialization="UTF-8,no BOM,LF,exact eight columns;shared importer compact JSON SHA-256 identity and identity ordering",
        original_date_semantics=True, publication_date_filter=False, rights="Private retrospective internal diagnostics only;prior source restrictions unchanged;no model-training/redistribution rights inferred"))
    return artifacts


def write_artifacts(artifacts, directory):
    directory = Path(directory).resolve()
    require(directory.is_relative_to(PRIVATE.resolve()) or directory.is_relative_to(Path(tempfile.gettempdir()).resolve()),
            "Output must remain private or temporary")
    paths = [directory / name for name in artifacts]
    check_overwrite(paths)
    directory.mkdir(parents=True, exist_ok=True)
    for name, raw in artifacts.items():
        with (directory / name).open("xb") as f:
            f.write(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    artifacts = build()
    if args.verify:
        for name, raw in artifacts.items():
            require((args.output / name).read_bytes() == raw, "Reproduction differs: " + name)
    else:
        write_artifacts(artifacts, args.output)
    print(json.dumps(dict(status="PASS", rows=10540, totals=EXPECTED,
                         artifacts={k: sha(v) for k, v in artifacts.items()}), sort_keys=True))


if __name__ == "__main__":
    main()
