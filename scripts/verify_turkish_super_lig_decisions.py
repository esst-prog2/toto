"""Independent Phase 3 reconciliation; no production adjudicator imported.

Reuses the existing independently implemented raw-source validator. Human-curated
historical facts are shared policy inputs, not independently repeated research.
No network, standardized data, production selection or naming helpers.
"""
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import argparse
import hashlib
import json
import tempfile

from scripts import validate_turkish_super_lig_structure as raw_validator

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/private/turkey/super_lig/phase3"
INVENTORY = PRIVATE.parent / "phase2/validated"
OUTPUT = PRIVATE / "accepted"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def serialize(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def load(path):
    return json.loads(path.read_bytes())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_decision(event, rows, decision, rule, evidence):
    """Reconcile choices directly with bound source observations / reviewed facts."""
    require(decision["source_ids"] == event["source_ids"], "Contributor mismatch")
    require(decision["season"] == event["season"] and
            decision["source_stage"] == event["stage"], "Season/stage mismatch")
    require(decision["prior_quarantined"] == event["quarantined"] and
            decision["source_issues"] == event["issues"], "Quarantine/issue history lost")
    if rule:
        require(rule["event_sha256"] == digest(serialize(event)), "Changed case binding")
        require(rule["source_ids"] == event["source_ids"], "Case membership changed")
        require(rule["season"] == event["season"] and rule["stage"] == event["stage"] and
                decision["reason"] == rule["kind"], "Case classification mismatch")
        fact = rule["fact_assertion"]
        require(fact["event_id"] == event["event_id"] and
                fact["season"] == event["season"], "Fact scope mismatch")
        anchor = next(r for r in rows if r["source_id"] == event["anchor"])
        require(fact["identity"] == [anchor["home"], anchor["away"]], "Fact identity mismatch")
        require(rule["accepted_date"] == fact["original_football_date"] and
                rule["accepted_score"] == fact["accepted_final_score"] and
                rule["completion_date"] == fact["completion_date"], "Fact/rule contradiction")
        action, day, score = rule["disposition"], fact["original_football_date"], fact["accepted_final_score"]
        require(decision["evidence_ids"] == rule["evidence_ids"], "Evidence reference mismatch")
        refs = [evidence[key] for key in decision["evidence_ids"]]
        require(bool(refs), "No evidence")
        if action != "HOLD_OUT":
            require(any(r["access"] in {"PRIMARY_DIRECT", "TFF_HOSTED_AGENCY_DIRECT",
                        "PRIMARY_PARTICIPANT_DIRECT", "PRIMARY_BROADCAST_DIRECT",
                        "SECONDARY_DIRECT", "PRESERVED_ORIGINAL_DIRECT"} for r in refs),
                    "Uninspected evidence cannot settle event")
        if action == "INCLUDE":
            require(fact["played"] is True, "Included no-kickoff event")
        if action == "NOT_PLAYED":
            require(fact["played"] is False, "Played event classified no-play")
    else:
        require(not decision["evidence_ids"], "Unbound historical override")
        score_set = set()
        exact_days = set()
        flag = event["quarantined"] or event["stage"] != "REGULAR_SEASON"
        for row in rows:
            if row["hg"] is not None:
                score_set.add((int(row["hg"]), int(row["ag"])))
                if row["date"]:
                    exact_days.add(row["date"])
            if row["source_status"] in ("AWARDED_DOCUMENTARY", "AWARDED_ANNOTATION",
                                         "ABANDONED_DOCUMENTARY", "ABANDONMENT_CONTEXT"):
                flag = True
        action = "INCLUDE" if not flag and len(score_set) == 1 and len(exact_days) == 1 else "HOLD_OUT"
        day = sorted(exact_days)[0] if action == "INCLUDE" else None
        score = list(sorted(score_set)[0]) if action == "INCLUDE" else None
    require(decision["disposition"] == action, "Unsupported disposition")
    chosen = decision["accepted"]
    if action != "INCLUDE":
        require(chosen is None, "Excluded values leaked into projection")
        return
    require(chosen["original_football_date"] == day and chosen["final_score"] == score,
            "Accepted historical values changed")
    require(all(type(n) is int and n >= 0 for n in score), "Invalid numeric score")
    d = date.fromisoformat(day)
    y = int(event["season"][:4])
    require(date(y, 7, 1) <= d <= (date(2020, 7, 26) if y == 2019 else date(y+1, 6, 30)),
            "Wrong-season date")
    require(chosen["identity_source_id"] == event["anchor"], "Unsupported identity source")
    require(chosen["date_source_ids"] == sorted(r["source_id"] for r in rows if r["date"] == day),
            "Date source provenance mismatch")
    require(chosen["score_source_ids"] == sorted(r["source_id"] for r in rows
            if r["hg"] is not None and [int(r["hg"]), int(r["ag"])] == score),
            "Score source provenance mismatch")
    require(chosen["completion_date"] == (rule["completion_date"] if rule else None),
            "Original kickoff/completion conflated")


def validate(directory=OUTPUT, *, check_raw=True):
    if check_raw:
        reconstructed = raw_validator.validate()
        require(serialize(reconstructed) == (INVENTORY / "independent_validation.json").read_bytes(),
                "Independent original reconstruction changed")
    inv = load(INVENTORY / "source_inventory.json")
    events = load(INVENTORY / "overlap_assessment.json")["conditional_events"]
    cases = load(PRIVATE / "case_rules.v2.json")
    evidence = load(PRIVATE / "evidence_index.v2.json")["entries"]
    contexts = load(PRIVATE / "context_assessments.json")
    registry = load(directory / "decision_registry.json")
    require(registry["case_rules_sha256"] == digest((PRIVATE / "case_rules.v2.json").read_bytes()),
            "Case facts changed")
    require(registry["evidence_index_sha256"] == digest((PRIVATE / "evidence_index.v2.json").read_bytes()),
            "Research evidence changed")
    require(registry["context_assessments_sha256"] == digest((PRIVATE / "context_assessments.json").read_bytes()),
            "Season context changed")
    require(registry["policy_version"] == cases["policy_version"], "Policy version mismatch")
    require(registry["policy"] == dict(original_football_date=True, accepted_final_result=True,
            administrative_publication_date_filter=False, no_kickoff="NOT_PLAYED",
            unresolved="HOLD_OUT", separate_optional_cup="OUT_OF_SCOPE",
            eligible_top_flight_league_postseason=True, cross_division="OUT_OF_SCOPE"),
            "Policy drift")
    for name, value in load(INVENTORY.parent / "final_status.json")["artifacts"].items():
        require(registry["input_sha256"][name] == value == digest((INVENTORY / name).read_bytes()),
                "Frozen inventory digest mismatch")
    for rec in inv["catalogue"]:
        require(registry["original_sha256"][rec["root_path"]] == rec["sha256"] ==
                digest((ROOT / rec["root_path"]).read_bytes()), "Original bytes changed")
    obs = {r["source_id"]: r for r in inv["observations"]}
    decisions = registry["decisions"]
    decision_ids = [d["event_id"] for d in decisions]
    require(len(decision_ids) == len(set(decision_ids)) == len(events) == 10574, "Population incomplete")
    require(set(decision_ids) == {e["event_id"] for e in events}, "Missing/extra event")
    byid = {d["event_id"]: d for d in decisions}
    require(Counter(s for d in decisions for s in d["source_ids"]) == Counter(obs.keys()),
            "Duplicate or omitted representation")
    for event in events:
        check_decision(event, [obs[s] for s in event["source_ids"]], byid[event["event_id"]],
                       cases["cases"].get(event["event_id"]), evidence)
    corrected = load(INVENTORY / "discrepancy_registry.json")["corrections"]
    source_event = {s: d for d in decisions for s in d["source_ids"]}
    require(len(corrected) == 143, "Recovery count drift")
    for row in corrected:
        require(row["original_fields"]["Date"] == row["reported_date"], "Original recovery date lost")
        require(row == obs[row["source_id"]], "Frozen correction metadata altered")
        d = source_event[row["source_id"]]
        require(d["disposition"] == "INCLUDE" and
                d["accepted"]["original_football_date"] == row["date"], "Recovery decision mismatch")
    quarantine = load(INVENTORY / "structural_checks.json")
    require(len(quarantine["quarantined_event_ids"]) == 13 and
            len(quarantine["all_structural_quarantine_source_ids"]) == 36, "Quarantine boundary changed")
    require({d["event_id"] for d in decisions if d["prior_quarantined"]} ==
            set(quarantine["quarantined_event_ids"]), "Incomplete quarantine decisions")
    for event_id in quarantine["quarantined_event_ids"]:
        require(event_id in cases["cases"] and byid[event_id]["disposition"] == "INCLUDE",
                "Quarantine silently restored or lost")
    frozen = [r for r in obs.values() if r["date_precision"] == "QUARANTINED_EXACT_DAY"]
    require(len(frozen) == 10 and all(r["date"] is None and r["quarantined"] for r in frozen),
            "Frozen ten-case source metadata edited")
    require(sum(d["reason"] == "RESOLVED_FROZEN_DATE" for d in decisions) == 10,
            "Wrong recovery resolution count")
    totals = dict(sorted(Counter(d["disposition"] for d in decisions).items()))
    require(registry["totals"] == totals, "Disposition totals mismatch")
    matrix = load(directory / "season_stage_decisions.json")["coverage"]
    original_matrix = load(INVENTORY / "season_stage_coverage.json")["coverage"]
    require(len(matrix) == 36 and [r["season"] for r in matrix] == [r["season"] for r in original_matrix],
            "Incomplete season matrix")
    for row, original in zip(matrix, original_matrix):
        subset = [d for d in decisions if d["season"] == row["season"]]
        stages = defaultdict(Counter)
        for d in subset:
            stages[d["source_stage"]][d["disposition"]] += 1
        require(row["events"] == len(subset) == sum(row["dispositions"].values()), "Season event count")
        require(row["dispositions"] == {k: sum(d["disposition"] == k for d in subset)
                for k in ("INCLUDE", "HOLD_OUT", "NOT_PLAYED", "OUT_OF_SCOPE")}, "Season decisions")
        require(row["stages"] == {k: dict(v) for k, v in stages.items()}, "Stage decisions")
        require(row["exact_date_gap"] == original["exact_date_gap"] and
                row["source_gap_slots"] == max(0, original["nominal_regular_slots"] -
                                                original["regular_conditional_events"]), "Coverage gaps changed")
    review = load(directory / "review_assessment.json")
    queue = load(INVENTORY / "review_queue.json")["items"]
    require(len(review["items"]) == len(queue) == 779 and
            {r["queue_id"] for r in review["items"]} == {r["queue_id"] for r in queue}, "Review queue incomplete")
    require(review["event_queue_items"] == 767 and review["context_queue_items"] == 12, "Review populations")
    for item in review["items"]:
        if item["kind"] == "CONDITIONAL_EVENT":
            require(item["disposition"] == byid[item["queue_id"]]["disposition"], "Queue disposition mismatch")
        else:
            for key, value in contexts[item["season"]].items():
                require(item[key] == value, "Context assessment mismatch")
            require(all(key in evidence for key in item["evidence_ids"]), "Unbound context evidence")
    for sample in review["deterministic_raw_sample"]:
        r = obs[sample["source_id"]]
        lines = (ROOT / r["source"]).read_bytes().splitlines(keepends=True)
        require(digest(b"".join(lines[r["line"]-1:r["end_line"]])) == sample["physical_sha256"],
                "Raw sample binding changed")
    require(len(review["deterministic_raw_sample"]) == 34, "Sampling scope drift")
    assessment = load(directory / "historical_assessment.json")
    require(assessment["totals"] == totals and assessment["conditional_events"] == 10574,
            "Historical assessment mismatch")
    require({d["event_id"] for d in assessment["targeted_cases"]} == set(cases["cases"]),
            "Missing targeted case assessment")
    # Duplicate accepted dates/identities would reintroduce overlap double counting.
    keys = []
    for d in decisions:
        if d["accepted"]:
            r = obs[d["accepted"]["identity_source_id"]]
            keys.append((d["season"], d["source_stage"], d["accepted"]["original_football_date"],
                         r["source"], r["home"], r["away"]))
    require(len(keys) == len(set(keys)), "Duplicate accepted historical identity")
    return dict(status="PASS", method="Independent raw Phase2 reconstruction plus independent Phase3 policy/fact reconciliation;no production adjudicator imported", historical_research_independence="Shared curated historical judgments;code independence does not certify external source lineage or independently repeat documentary research", originals=26, observations=13894, events=10574, totals=totals, frozen_corrections=143, structural_quarantines=13, structural_quarantine_representations=36, frozen_quarantine_resolutions=10, review_events=767, review_contexts=12, raw_spot_samples=34, duplicate_accepted_identities=0, raw_reconstruction_checked=check_raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    dest = args.directory.resolve()
    require(any(dest.is_relative_to(p.resolve()) for p in
                (PRIVATE, Path(tempfile.gettempdir()), Path("/private/tmp"))), "Private outputs only")
    result = validate(dest)
    raw = serialize(result)
    target = dest / "independent_decision_validation.json"
    if args.verify:
        require(target.read_bytes() == raw, "Independent assessment not reproducible")
    else:
        with target.open("xb") as f:
            f.write(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
