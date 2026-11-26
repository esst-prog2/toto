"""Offline Turkish Phase 3 decisions, never standardized match output.

The frozen Phase 2 event population is authoritative membership, not historical
truth. Targeted, private case facts override source values only in this registry.
Original observations, recovery metadata and quarantine history remain untouched.
"""
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import argparse
import json
import tempfile

from scripts import collect_turkish_super_lig_sources as acquisition

ROOT = acquisition.ROOT
PRIVATE = ROOT / "data/private/turkey/super_lig/phase3"
INVENTORY = PRIVATE.parent / "phase2/validated"
OUTPUT = PRIVATE / "accepted"
NAMES = ("decision_registry.json", "historical_assessment.json",
         "season_stage_decisions.json", "review_assessment.json")
DISPOSITIONS = ("INCLUDE", "HOLD_OUT", "NOT_PLAYED", "OUT_OF_SCOPE")
DIRECT = {"PRIMARY_DIRECT", "TFF_HOSTED_AGENCY_DIRECT",
          "PRIMARY_PARTICIPANT_DIRECT", "PRIMARY_BROADCAST_DIRECT",
          "SECONDARY_DIRECT", "PRESERVED_ORIGINAL_DIRECT"}


def read(path):
    return json.loads(path.read_bytes())


def validate_case(event, case, evidence):
    if case["event_sha256"] != acquisition.sha(acquisition.encode(event)):
        raise ValueError("Case event binding changed")
    if case["source_ids"] != event["source_ids"]:
        raise ValueError("Case contributor binding changed")
    fact = case["fact_assertion"]
    if fact["event_id"] != event["event_id"] or fact["season"] != event["season"]:
        raise ValueError("Case fact scope changed")
    if (case["accepted_date"], case["accepted_score"], case["completion_date"]) != (
            fact["original_football_date"], fact["accepted_final_score"], fact["completion_date"]):
        raise ValueError("Case fact contradiction")
    if case["disposition"] not in DISPOSITIONS or not case["evidence_ids"]:
        raise ValueError("Missing disposition/evidence")
    refs = [evidence[key] for key in case["evidence_ids"]]
    if case["disposition"] != "HOLD_OUT" and not any(
            ref["access"] in DIRECT for ref in refs):
        raise ValueError("Search-only evidence cannot settle a material case")
    if case["disposition"] == "INCLUDE":
        if not case["fact_assertion"]["played"]:
            raise ValueError("No-kickoff fixture cannot be included")
        date.fromisoformat(case["accepted_date"])
        score = case["accepted_score"]
        if not isinstance(score, list) or len(score) != 2 or any(
                type(n) is not int or n < 0 for n in score):
            raise ValueError("Invalid accepted score")
        if case["completion_date"] and case["completion_date"] < case["accepted_date"]:
            raise ValueError("Completion precedes original kickoff")
    elif case["accepted_date"] is not None or case["accepted_score"] is not None:
        raise ValueError("Excluded event cannot have accepted output values")
    if case["disposition"] == "NOT_PLAYED" and fact["played"] is not False:
        raise ValueError("Played event cannot be classified no-play")


def decide(event, members, case=None, evidence=None):
    """A case wins over ordinary-source selection; quarantines fail closed."""
    day = score = completion = None
    refs = []
    if case is not None:
        validate_case(event, case, evidence)
        disposition, reason = case["disposition"], case["kind"]
        day, score, completion = (case[k] for k in
                                 ("accepted_date", "accepted_score", "completion_date"))
        refs = case["evidence_ids"]
    else:
        scored = [r for r in members if r["date"] and r["hg"] is not None]
        dates = {r["date"] for r in scored}
        scores = {(int(r["hg"]), int(r["ag"])) for r in members
                  if r["hg"] is not None}
        exceptional = any(r["source_status"] in {
            "AWARDED_DOCUMENTARY", "AWARDED_ANNOTATION", "ABANDONED_DOCUMENTARY",
            "ABANDONMENT_CONTEXT"} for r in members)
        if event["stage"] != "REGULAR_SEASON":
            disposition, reason = "HOLD_OUT", "UNREVIEWED_STAGE"
        elif event["quarantined"]:
            disposition, reason = "HOLD_OUT", "UNRESOLVED_STRUCTURAL_QUARANTINE"
        elif exceptional:
            disposition, reason = "HOLD_OUT", "UNREVIEWED_PLAY_OR_FINALITY"
        elif len(dates) == len(scores) == 1:
            disposition, reason = "INCLUDE", "SUPPORTED_ORDINARY_SOURCE_RESULT"
            day, score = next(iter(dates)), list(next(iter(scores)))
        else:
            disposition, reason = "HOLD_OUT", "NO_SUPPORTED_EXACT_DATE_AND_RESULT"
    accepted = None
    if disposition == "INCLUDE":
        accepted = dict(original_football_date=day, final_score=score,
                        completion_date=completion,
                        identity_source_id=event["anchor"],
                        date_source_ids=sorted(r["source_id"] for r in members
                                               if r["date"] == day),
                        score_source_ids=sorted(r["source_id"] for r in members
                                                if r["hg"] is not None and
                                                [int(r["hg"]), int(r["ag"])] == score))
    return dict(event_id=event["event_id"], season=event["season"],
                source_stage=event["stage"], source_ids=event["source_ids"],
                disposition=disposition, reason=reason, accepted=accepted,
                evidence_ids=refs, prior_quarantined=event["quarantined"],
                source_issues=event["issues"],
                evidence_scope="TARGETED_DOCUMENTARY_REVIEW" if case else
                "FROZEN_SOURCE_DESCRIPTION;NO_EVENT_BY_EVENT_EXTERNAL_CERTIFICATION")


def build():
    final = read(INVENTORY.parent / "final_status.json")
    inputs = {}
    for name, expected in final["artifacts"].items():
        raw = (INVENTORY / name).read_bytes()
        if acquisition.sha(raw) != expected:
            raise ValueError("Approved Phase 2 artifact changed: " + name)
        inputs[name] = expected
    inv = read(INVENTORY / "source_inventory.json")
    overlap = read(INVENTORY / "overlap_assessment.json")
    events = overlap["conditional_events"]
    obs = {r["source_id"]: r for r in inv["observations"]}
    cases = read(PRIVATE / "case_rules.v2.json")
    evidence = read(PRIVATE / "evidence_index.v2.json")["entries"]
    event_ids = {e["event_id"] for e in events}
    if len(events) != len(event_ids) or not set(cases["cases"]) <= event_ids:
        raise ValueError("Duplicate or orphan event/case")
    if len(events) != 10574 or len(obs) != 13894 or len(inv["catalogue"]) != 26:
        raise ValueError("Frozen population changed")
    decisions = [decide(e, [obs[s] for s in e["source_ids"]],
                        cases["cases"].get(e["event_id"]), evidence)
                 for e in sorted(events, key=lambda e: e["event_id"])]
    if Counter(s for d in decisions for s in d["source_ids"]) != Counter(obs.keys()):
        raise ValueError("Incomplete or duplicate source representation")
    totals = dict(sorted(Counter(d["disposition"] for d in decisions).items()))
    byid = {d["event_id"]: d for d in decisions}
    coverage = read(INVENTORY / "season_stage_coverage.json")
    matrix = []
    for row in coverage["coverage"]:
        subset = [d for d in decisions if d["season"] == row["season"]]
        stages = defaultdict(Counter)
        for d in subset:
            stages[d["source_stage"]][d["disposition"]] += 1
        matrix.append(dict(season=row["season"], events=len(subset),
                           dispositions={k: sum(d["disposition"] == k for d in subset)
                                         for k in DISPOSITIONS},
                           stages={k: dict(sorted(v.items())) for k, v in sorted(stages.items())},
                           exact_date_gap=row["exact_date_gap"],
                           nominal_regular_slots=row["nominal_regular_slots"],
                           source_gap_slots=max(0, row["nominal_regular_slots"] -
                                                row["regular_conditional_events"])))
    # Small, reproducible raw-source spot sample: one ordinary event per represented
    # season, plus one in each early undated season. Not external certification.
    samples = []
    for season in sorted({e["season"] for e in events}):
        pool = [e for e in events if e["season"] == season and
                not e["issues"] and e["stage"] == "REGULAR_SEASON" and
                e["event_id"] not in cases["cases"]]
        if pool:
            chosen = min(pool, key=lambda e: e["event_id"])
            anchor = obs[chosen["anchor"]]
            samples.append(dict(event_id=chosen["event_id"], season=season,
                                source_id=anchor["source_id"], source=anchor["source"],
                                line=anchor["line"], end_line=anchor["end_line"],
                                physical_sha256=anchor["physical_sha256"],
                                checks="Raw identity,date precision,score,stage;independent raw parser reconciles fields"))
    queue = read(INVENTORY / "review_queue.json")
    contexts = read(PRIVATE / "context_assessments.json")
    if set(contexts) != {q["season"] for q in queue["items"] if q["kind"] == "SEASON_CONTEXT"}:
        raise ValueError("Season-context assessment incomplete")
    reviews = []
    for item in queue["items"]:
        if item["kind"] == "CONDITIONAL_EVENT":
            d = byid[item["queue_id"]]
            method = ("TARGETED_CASE" if d["evidence_ids"] else
                      "RETAIN_DATE_GAP" if d["disposition"] == "HOLD_OUT" else
                      "SOURCE_FIELD_REVIEW_AND_INDEPENDENT_STRUCTURAL_CHECK")
            reviews.append(dict(queue_id=item["queue_id"], kind=item["kind"],
                                categories=item["categories"], method=method,
                                disposition=d["disposition"], decision_event_id=d["event_id"]))
        else:
            reviews.append(dict(queue_id=item["queue_id"], kind=item["kind"],
                                season=item["season"], method="SEASON_CONTEXT_AND_FROZEN_COVERAGE",
                                **contexts[item["season"]]))
    corrections = read(INVENTORY / "discrepancy_registry.json")["corrections"]
    corrected_sources = {r["source_id"] for r in corrections}
    correction_events = [d for d in decisions if corrected_sources.intersection(d["source_ids"])]
    if len(corrections) != 143 or len(correction_events) != 143:
        raise ValueError("Recovery population changed")
    source_bindings = {r["root_path"]: r["sha256"] for r in inv["catalogue"]}
    registry = dict(phase=3, policy_version=cases["policy_version"],
                    policy=dict(original_football_date=True, accepted_final_result=True,
                                administrative_publication_date_filter=False,
                                no_kickoff="NOT_PLAYED", unresolved="HOLD_OUT",
                                separate_optional_cup="OUT_OF_SCOPE",
                                eligible_top_flight_league_postseason=True,
                                cross_division="OUT_OF_SCOPE"),
                    input_sha256=inputs, original_sha256=source_bindings,
                    evidence_index_sha256=acquisition.sha((PRIVATE / "evidence_index.v2.json").read_bytes()),
                    case_rules_sha256=acquisition.sha((PRIVATE / "case_rules.v2.json").read_bytes()),
                    context_assessments_sha256=acquisition.sha((PRIVATE / "context_assessments.json").read_bytes()),
                    observation_reference="source_inventory.json bound above;all original fields/physical locators retained there",
                    totals=totals, decisions=decisions)
    historical = dict(status="PASS_WITH_CONTAINED_HOLDS", totals=totals,
                      original_count=26, observations=13894, conditional_events=10574,
                      explicit_cases=len(cases["cases"]), documentary_evidence_entries=len(evidence),
                      corrected_recovery_observations=143,
                      correction_event_dispositions=dict(Counter(d["disposition"] for d in correction_events)),
                      prior_quarantine_outcomes=[d for d in decisions if d["prior_quarantined"]],
                      targeted_cases=[d for d in decisions if d["evidence_ids"]],
                      gaps=dict(early_exact_dates=["1990/1991", "1991/1992", "1992/1993", "1993/1994"],
                                omitted_2009_regular_slots=34,
                                omitted_2009_context="Four played later-awarded and30no-kickoff;not added to frozen event population",
                                missing_2011_eligible_playoff_fixture_descriptions=24,
                                excluded_2011_optional_cup_group_expectation=24,
                                missing_is_not_not_played=True),
                      limitations=["Most events remain single-source;known shared upstreams not independent historical proof",
                                   "No exhaustive legal finality research on every ordinary fixture",
                                   "Two older award-date cases and one abandoned original remain HOLD_OUT",
                                   "Research notes frozen offline;live page bytes not acquired or certified",
                                   "No new rights,redistribution or training permission;all detail private"])
    return dict(zip(NAMES, [registry, historical, dict(coverage=matrix),
                           dict(event_queue_items=queue["event_items"],
                                context_queue_items=queue["context_items"],
                                items=reviews, deterministic_raw_sample=samples,
                                sample_scope="One per represented season;raw spot review,not independent historical certification",
                                extreme_score_policy="Magnitude alone is not a defect;raw score fields and exceptional-case screen checked")]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    dest = args.output.resolve()
    if not any(dest.is_relative_to(p.resolve()) for p in
               (PRIVATE, Path(tempfile.gettempdir()), Path("/private/tmp"))):
        raise ValueError("Private or temporary outputs only")
    artifacts = build()
    if not args.verify and any((dest / name).exists() for name in NAMES):
        raise FileExistsError("Frozen Phase 3 output already exists")
    for name, value in artifacts.items():
        raw = acquisition.encode(value)
        if args.verify:
            if (dest / name).read_bytes() != raw:
                raise ValueError("Nonreproducible artifact: " + name)
        else:
            acquisition.save(dest / name, raw)
    print(json.dumps({"artifacts": len(artifacts), "totals": artifacts[NAMES[0]]["totals"]}))


if __name__ == "__main__":
    main()
