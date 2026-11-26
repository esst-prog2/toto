"""Synthetic Phase 4 projection and independent-verification safeguards."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import standardize_turkish_super_lig_results as production
from scripts import verify_turkish_super_lig_standardization as independent


class TurkishStandardizationTests(unittest.TestCase):
    def setUp(self):
        self.source = dict(source_id="synthetic-row", season="2019/2020", stage="REGULAR_SEASON",
                           home="Synthetic Home", away="Synthetic Away")
        self.observations = {"synthetic-row": self.source}
        self.decision = dict(event_id="synthetic-event", season="2019/2020",
            source_stage="REGULAR_SEASON", source_ids=["synthetic-row"], disposition="INCLUDE",
            accepted=dict(identity_source_id="synthetic-row", original_football_date="2020-07-26",
                          completion_date=None, final_score=[2, 1]))

    def project(self):
        return production.project(self.decision, self.observations)

    def row(self, day="2020-07-26", home="Synthetic Home", away="Synthetic Away", score=(2, 1)):
        return independent.make_row("2019/2020", day, home, away, list(score))

    def test_shared_importer_preserves_covid_extension(self):
        raw, rows, summary = production.convert([self.project()])
        self.assertEqual(rows, [self.row()])
        self.assertEqual(raw, independent.csv_bytes([self.row()]))
        self.assertEqual(summary["accepted"], 1)

    def test_original_kickoff_wins_over_completion(self):
        self.decision["accepted"].update(original_football_date="2020-03-10", completion_date="2020-06-10")
        self.assertEqual(self.project()["date"], "2020-03-10")

    def test_three_exclusion_dispositions_cannot_project(self):
        for action in ("HOLD_OUT", "NOT_PLAYED", "OUT_OF_SCOPE"):
            with self.subTest(action=action):
                self.decision.update(disposition=action, accepted=None)
                self.assertIsNone(self.project())

    def test_excluded_accepted_values_are_rejected(self):
        self.decision["disposition"] = "HOLD_OUT"
        with self.assertRaisesRegex(ValueError, "Excluded"):
            self.project()

    def test_unapproved_stage_rejected(self):
        self.decision["source_stage"] = "CROSS_DIVISION"
        with self.assertRaisesRegex(ValueError, "stage"):
            self.project()

    def test_identity_must_be_bound_contributor(self):
        self.decision["source_ids"] = ["another-row"]
        with self.assertRaisesRegex(ValueError, "identity anchor"):
            self.project()

    def test_identity_season_must_agree(self):
        self.source["season"] = "2018/2019"
        with self.assertRaisesRegex(ValueError, "identity anchor"):
            self.project()

    def test_unapproved_season_rejected(self):
        self.decision["season"] = "1990/1991"
        with self.assertRaisesRegex(ValueError, "season"):
            self.project()

    def test_wrong_season_date_rejected(self):
        self.decision["accepted"]["original_football_date"] = "2020-08-01"
        with self.assertRaisesRegex(ValueError, "season window"):
            self.project()

    def test_negative_and_boolean_goals_rejected(self):
        for score in ([True, 0], [-1, 0]):
            self.decision["accepted"]["final_score"] = score
            with self.assertRaisesRegex(ValueError, "goals"):
                self.project()

    def test_no_source_name_trimming_or_alias_guess(self):
        self.source["home"] = " Synthetic Home "
        with self.assertRaisesRegex(ValueError, "opponents"):
            self.project()

    def test_distinct_opponents_cannot_collapse(self):
        self.source["away"] = self.source["home"]
        with self.assertRaisesRegex(ValueError, "opponents"):
            self.project()

    def test_same_identity_cannot_hide_score_conflict(self):
        first = self.project()
        second = dict(first, home_goals=3)
        with self.assertRaisesRegex(ValueError, "collide"):
            production.convert([first, second])

    def test_rematches_on_different_dates_remain_distinct(self):
        first = self.project()
        second = dict(first, date="2020-07-25")
        raw, rows, summary = production.convert([first, second])
        self.assertEqual(len({r["match_id"] for r in rows}), 2)
        self.assertEqual(independent.check_csv(raw, [self.row(), self.row("2020-07-25")]), rows)

    def test_independent_unicode_and_quoting_bytes(self):
        row = self.row(home='Synthetic "É", Team')
        projection = {k:v for k,v in row.items() if k != "match_id"}
        raw, rows, _ = production.convert([projection])
        self.assertEqual(raw, independent.csv_bytes([row]))
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\n", raw)

    def test_wrong_id_is_rejected_independently(self):
        bad = dict(self.row(), match_id="0"*64)
        with self.assertRaisesRegex(ValueError, "match ID"):
            independent.check_csv(independent.csv_bytes([bad]), [self.row()])

    def test_missing_and_extra_rows_rejected_independently(self):
        for rows in ([], [self.row(), self.row("2020-07-25")]):
            with self.assertRaisesRegex(ValueError, "Missing/extra"):
                independent.check_csv(independent.csv_bytes(rows), [self.row()])

    def test_duplicate_row_rejected_independently(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            independent.check_csv(independent.csv_bytes([self.row(), self.row()]), [self.row()])

    def test_score_tamper_rejected_with_valid_identity(self):
        changed = dict(self.row(), away_goals=3)
        with self.assertRaisesRegex(ValueError, "bytes/fields"):
            independent.check_csv(independent.csv_bytes([changed]), [self.row()])

    def test_orientation_tamper_rejected_with_valid_identity(self):
        changed = self.row(home="Synthetic Away", away="Synthetic Home", score=(1, 2))
        with self.assertRaisesRegex(ValueError, "bytes/fields"):
            independent.check_csv(independent.csv_bytes([changed]), [self.row()])

    def test_wrong_column_order_rejected(self):
        raw = independent.csv_bytes([self.row()]).replace(b"match_id,date,league", b"date,match_id,league", 1)
        with self.assertRaisesRegex(ValueError, "schema"):
            independent.check_csv(raw, [self.row()])

    def test_noncanonical_goals_rejected(self):
        raw = independent.csv_bytes([self.row()]).replace(b",2,1\n", b",02,1\n")
        with self.assertRaisesRegex(ValueError, "integer"):
            independent.check_csv(raw, [self.row()])

    def test_whitespace_or_bom_serialization_tamper_rejected(self):
        raw = independent.csv_bytes([self.row()])
        for bad in (raw.replace(b"\n", b"\r\n"), b"\xef\xbb\xbf"+raw):
            with self.assertRaises(ValueError):
                independent.check_csv(bad, [self.row()])

    def test_explicit_approval_scope_required(self):
        with self.assertRaisesRegex(ValueError, "approval"):
            production.compose({}, {}, {}, dict(phase=4, scope="NOT_APPROVED"))

    def test_output_overwrite_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            production.write_artifacts({"synthetic.json": b"original"}, Path(temp))
            with self.assertRaises(FileExistsError):
                production.write_artifacts({"synthetic.json": b"changed"}, Path(temp))
            self.assertEqual((Path(temp)/"synthetic.json").read_bytes(), b"original")


if __name__ == "__main__":
    unittest.main()
