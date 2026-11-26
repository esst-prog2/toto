"""Synthetic policy and adverse independent-check cases; no private fixtures."""
import unittest

from scripts import adjudicate_turkish_super_lig as production
from scripts import verify_turkish_super_lig_decisions as independent


class TurkishDecisionsTest(unittest.TestCase):
    def setUp(self):
        self.row = dict(source_id="synthetic-source", date="2020-02-01", hg="2", ag="1",
                        home="Synthetic Home", away="Synthetic Away", source_status="SCORED")
        self.event = dict(event_id="synthetic-event", season="2019/2020", stage="REGULAR_SEASON",
                          source_ids=[self.row["source_id"]], anchor=self.row["source_id"],
                          quarantined=False, issues=[])
        self.evidence = {"E": dict(access="PRIMARY_DIRECT", published="2020-05-01")}

    def case(self, disposition="INCLUDE", *, played=True, day="2020-02-01", score=None,
             completion=None):
        if score is None and disposition == "INCLUDE":
            score = [3, 0]
        if disposition != "INCLUDE":
            day = score = None
        fact = dict(event_id=self.event["event_id"], season=self.event["season"],
                    identity=[self.row["home"], self.row["away"]], played=played,
                    original_football_date=day, accepted_final_score=score,
                    completion_date=completion)
        return dict(event_sha256=independent.digest(independent.serialize(self.event)),
                    source_ids=self.event["source_ids"], disposition=disposition,
                    season=self.event["season"], stage=self.event["stage"],
                    kind="SYNTHETIC_REVIEW", evidence_ids=["E"], accepted_date=day,
                    accepted_score=score, completion_date=completion, fact_assertion=fact)

    def check(self, decision, rule=None, rows=None):
        independent.check_decision(self.event, rows or [self.row], decision, rule, self.evidence)

    def test_ordinary_supported_result(self):
        d = production.decide(self.event, [self.row])
        self.assertEqual(d["disposition"], "INCLUDE")
        self.check(d)

    def test_unscored_schedule_does_not_replace_scored_date(self):
        schedule = dict(self.row, source_id="schedule", date="2020-02-02", hg=None,
                        ag=None, source_status="UNSCORED")
        self.event["source_ids"].append("schedule")
        d = production.decide(self.event, [self.row, schedule])
        self.assertEqual(d["accepted"]["original_football_date"], "2020-02-01")
        self.check(d, rows=[self.row, schedule])

    def test_scored_date_conflict_fails_closed(self):
        other = dict(self.row, source_id="other", date="2020-02-02")
        self.event["source_ids"].append("other")
        d = production.decide(self.event, [self.row, other])
        self.assertEqual(d["disposition"], "HOLD_OUT")
        self.check(d, rows=[self.row, other])

    def test_quarantine_cannot_restore_from_another_representation(self):
        self.event["quarantined"] = True
        d = production.decide(self.event, [self.row])
        self.assertEqual(d["disposition"], "HOLD_OUT")
        self.check(d)

    def test_undated_result_is_not_invented_not_played(self):
        self.row["date"] = None
        d = production.decide(self.event, [self.row])
        self.assertEqual(d["disposition"], "HOLD_OUT")
        self.check(d)

    def test_unreviewed_award_is_held(self):
        self.row["source_status"] = "AWARDED_DOCUMENTARY"
        d = production.decide(self.event, [self.row])
        self.assertEqual(d["disposition"], "HOLD_OUT")
        self.check(d)

    def test_later_final_award_keeps_original_football_date(self):
        rule = self.case()
        d = production.decide(self.event, [self.row], rule, self.evidence)
        self.assertEqual(d["accepted"]["final_score"], [3, 0])
        self.assertEqual(d["accepted"]["original_football_date"], "2020-02-01")
        self.assertEqual(d["accepted"]["score_source_ids"], [])
        self.check(d, rule)

    def test_no_kickoff_is_not_played(self):
        rule = self.case("NOT_PLAYED", played=False)
        d = production.decide(self.event, [self.row], rule, self.evidence)
        self.assertIsNone(d["accepted"])
        self.check(d, rule)

    def test_independent_check_rejects_played_no_play(self):
        rule = self.case("NOT_PLAYED", played=False)
        d = production.decide(self.event, [self.row], rule, self.evidence)
        rule["fact_assertion"]["played"] = True
        with self.assertRaisesRegex(ValueError, "Played event"):
            self.check(d, rule)

    def test_search_only_cannot_settle_case(self):
        self.evidence["E"]["access"] = "SEARCH_INDEX_ONLY"
        with self.assertRaisesRegex(ValueError, "Search-only"):
            production.decide(self.event, [self.row], self.case(), self.evidence)

    def test_case_cannot_float_to_another_source_population(self):
        rule = self.case()
        self.event["source_ids"].append("new contributor")
        with self.assertRaisesRegex(ValueError, "binding"):
            production.decide(self.event, [self.row], rule, self.evidence)

    def test_unknown_stage_requires_review(self):
        self.event["stage"] = "UNKNOWN_FINAL"
        self.assertEqual(production.decide(self.event, [self.row])["disposition"], "HOLD_OUT")

    def test_resumption_preserves_two_dates(self):
        rule = self.case(completion="2020-02-02")
        d = production.decide(self.event, [self.row], rule, self.evidence)
        self.assertEqual(d["accepted"]["original_football_date"], "2020-02-01")
        self.assertEqual(d["accepted"]["completion_date"], "2020-02-02")
        self.check(d, rule)

    def test_impossible_completion_rejected(self):
        with self.assertRaisesRegex(ValueError, "Completion"):
            production.decide(self.event, [self.row], self.case(completion="2020-01-31"), self.evidence)

    def test_independent_check_rejects_administrative_date_substitution(self):
        rule = self.case()
        d = production.decide(self.event, [self.row], rule, self.evidence)
        d["accepted"]["original_football_date"] = self.evidence["E"]["published"]
        with self.assertRaisesRegex(ValueError, "historical values"):
            self.check(d, rule)

    def test_independent_check_rejects_lost_contributor(self):
        d = production.decide(self.event, [self.row])
        d["source_ids"] = []
        with self.assertRaisesRegex(ValueError, "Contributor"):
            self.check(d)

    def test_invalid_score_rejected(self):
        with self.assertRaisesRegex(ValueError, "score"):
            production.decide(self.event, [self.row], self.case(score=[-1, 0]), self.evidence)

    def test_excluded_values_cannot_leak(self):
        rule = self.case("OUT_OF_SCOPE")
        d = production.decide(self.event, [self.row], rule, self.evidence)
        d["accepted"] = {"final_score": [2, 1]}
        with self.assertRaisesRegex(ValueError, "leaked"):
            self.check(d, rule)

    def test_shared_fact_contradiction_detected_independently(self):
        rule = self.case()
        d = production.decide(self.event, [self.row], rule, self.evidence)
        rule["fact_assertion"]["accepted_final_score"] = [0, 0]
        with self.assertRaisesRegex(ValueError, "contradiction"):
            self.check(d, rule)


if __name__ == "__main__":
    unittest.main()
