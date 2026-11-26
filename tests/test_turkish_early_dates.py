"""Synthetic adverse cases for the private early-date supplemental workflow."""
from copy import deepcopy
import unittest

from scripts import recover_turkish_early_dates as production
from scripts import verify_turkish_early_dates as independent


def fixture_html(*, day="14.02.1993", score=(2, 1), mid="synthetic001"):
    return (f'<tr class="haftaninMaclariTr">'
            f'<td class="haftaninMaclariTarih"><span id="x_lblTarih">{day}</span> 15:30</td>'
            '<td class="haftaninMaclariEv">Synthetic Home</td>'
            f'<td class="haftaninMaclariSkor"><a href="Default.aspx?macId={mid}">{score[0]} - {score[1]}</a></td>'
            '<td class="haftaninMaclariDeplasman">Synthetic Away</td>'
            f'<td class="haftaninMaclariDetay"><a href="Default.aspx?macId={mid}">Details</a></td></tr>')


class EarlyDateChecks(unittest.TestCase):
    def setUp(self):
        self.source = dict(season="1992/1993", stage="REGULAR_SEASON", round=19,
                           home="Home raw", away="Away raw", hg="2", ag="1",
                           nominal_date_heading="13-14 February 1993")
        self.target = dict(source_observation=self.source)
        self.mapping = {"Home raw": "Synthetic Home", "Away raw": "Synthetic Away"}
        self.fixture = dict(season="1992/1993", stage="REGULAR_SEASON", round=19,
                            home="Synthetic Home", away="Synthetic Away", score=[2, 1],
                            date="1993-02-14", tff_match_id="001")

    def assess(self, fixtures=None, mapping=None):
        return production.assess_target(self.target, fixtures or [self.fixture],
                                        self.mapping if mapping is None else mapping)

    def test_exact_directed_fixture_qualifies(self):
        self.assertEqual(self.assess()["proposed_date"], "1993-02-14")

    def test_round_heading_is_not_used_to_infer_day(self):
        self.source["nominal_date_heading"] = "Wrong/ambiguous documentary heading"
        self.assertEqual(self.assess()["proposed_date"], self.fixture["date"])

    def test_reversed_home_away_fails_closed(self):
        f = dict(self.fixture, home=self.fixture["away"], away=self.fixture["home"])
        self.assertEqual(self.assess([f])["proposed_disposition"], "HOLD_OUT")

    def test_same_clubs_score_in_other_season_cannot_link(self):
        self.assertEqual(self.assess([dict(self.fixture, season="1993/1994")])["proposed_disposition"], "HOLD_OUT")

    def test_other_stage_cannot_link(self):
        self.assertEqual(self.assess([dict(self.fixture, stage="CUP")])["proposed_disposition"], "HOLD_OUT")

    def test_score_conflict_requires_explicit_review(self):
        d = self.assess([dict(self.fixture, score=[1, 1])])
        self.assertEqual(d["reason"], "SOURCE_SCORE_CONFLICT")
        self.assertIsNone(d["proposed_date"])

    def test_unknown_club_does_not_get_city_alias(self):
        self.assertEqual(self.assess(mapping={})["reason"], "UNRESOLVED_SOURCE_IDENTITY")

    def test_duplicate_candidates_cannot_supply_date(self):
        d = self.assess([self.fixture, dict(self.fixture, tff_match_id="002")])
        self.assertEqual(d["reason"], "MISSING_OR_AMBIGUOUS_DIRECTED_FIXTURE")

    def test_wrong_round_identity_is_not_silently_accepted(self):
        d = self.assess([dict(self.fixture, round=23)])
        self.assertEqual(d["reason"], "SOURCE_ROUND_IDENTITY_CONFLICT")

    def test_source_fields_remain_unchanged(self):
        before = deepcopy(self.target)
        self.assess()
        self.assertEqual(self.target, before)

    def repair(self):
        original = dict(self.source, source_id="synthetic-source")
        candidate = dict(self.fixture, score=[1, 1])
        detail = {k:candidate[k] for k in ("date", "home", "away", "score")}
        rule = dict(source_id=original["source_id"], repair_kind="SCORE_CORRECTION",
                    source_observation_sha256=independent.sha(independent.enc(original)),
                    proposed_fields=detail)
        return original, rule, candidate, detail

    def test_bound_score_repair_preserves_identity(self):
        production.validate_repair(*self.repair(), self.mapping)

    def test_changed_original_invalidates_repair(self):
        original, rule, candidate, detail = self.repair()
        original["ag"] = "9"
        with self.assertRaisesRegex(ValueError, "binding"):
            production.validate_repair(original, rule, candidate, detail, self.mapping)

    def test_score_repair_cannot_change_opponent(self):
        original, rule, candidate, detail = self.repair()
        candidate["away"] = detail["away"] = "Different away club"
        with self.assertRaisesRegex(ValueError, "scope"):
            production.validate_repair(original, rule, candidate, detail, self.mapping)

    def test_match_detail_disagreement_rejects_repair(self):
        original, rule, candidate, detail = self.repair()
        detail = dict(detail, date="1993-02-15")
        with self.assertRaisesRegex(ValueError, "Official"):
            production.validate_repair(original, rule, candidate, detail, self.mapping)

    def test_repair_cannot_change_season(self):
        original, rule, candidate, detail = self.repair()
        candidate["season"] = "1993/1994"
        with self.assertRaisesRegex(ValueError, "season"):
            production.validate_repair(original, rule, candidate, detail, self.mapping)

    def page(self):
        rows = [fixture_html(mid=str(n)) for n in range(8)]
        return ('<title>1992-1993 Sezonu</title><b>19.Hafta</b>' + '\n'.join(rows)).encode("iso-8859-9")

    def item(self):
        return dict(season="1992/1993", round=19, path="synthetic.html",
                    url="https://www.tff.org/Default.aspx?hafta=19&pageID=560")

    def test_two_independent_parsers_agree_on_explicit_fields(self):
        raw = self.page()
        p = production.parse_tff(raw, self.item(), dict(sha256=independent.sha(raw)))
        v = independent.parse(raw, self.item())
        self.assertEqual(p, v)

    def test_source_title_does_not_override_wrong_tier_url(self):
        item = dict(self.item(), url="https://www.tff.org/Default.aspx?hafta=19&pageID=790")
        with self.assertRaisesRegex(ValueError, "top-division"):
            production.parse_tff(self.page(), item, dict(sha256="synthetic"))

    def test_missing_fixture_date_is_not_filled_from_page_heading(self):
        raw = self.page().replace(b'14.02.1993', b'')
        with self.assertRaises(ValueError):
            production.parse_tff(raw, self.item(), dict(sha256="synthetic"))

    def test_wrong_selected_round_rejected(self):
        with self.assertRaisesRegex(ValueError, "round"):
            production.parse_tff(self.page(), dict(self.item(), round=20), dict(sha256="synthetic"))

    def test_wrong_season_page_rejected(self):
        raw = self.page().replace(b'1992-1993', b'1993-1994')
        with self.assertRaisesRegex(ValueError, "season"):
            production.parse_tff(raw, self.item(), dict(sha256="synthetic"))

    def test_duplicate_primary_identity_rejected(self):
        raw = self.page().replace(b'macId=7', b'macId=6')
        with self.assertRaisesRegex(ValueError, "distinct"):
            production.parse_tff(raw, self.item(), dict(sha256="synthetic"))

    def panel(self, competition="Synthetic Lig (Profesyonel Takım)"):
        vals = dict(lnkTakim1="Synthetic Home", lnkTakim2="Synthetic Away", lblTakim1Skor="2",
                    Label12="1", lblTarih="14.02.1993 - 15:30", lblOrganizasyonAdi=competition)
        return ''.join(f'<span id="x_MacBilgiDisplay1_dtMacBilgisi_{k}">{v}</span>'
                       for k, v in vals.items()).encode("iso-8859-9")

    def test_professional_detail_parsers_agree(self):
        raw = self.panel()
        parser = independent.Detail()
        parser.feed(raw.decode("iso-8859-9"))
        self.assertEqual(production.parse_match_detail(raw), parser.result())

    def test_same_day_youth_match_rejected(self):
        with self.assertRaisesRegex(ValueError, "professional"):
            production.parse_match_detail(self.panel("Paf Ligi (PAF Takımı)"))

    def test_detail_without_final_score_rejected(self):
        raw = self.panel().replace(b'_Label12">1', b'_Label12">-')
        with self.assertRaisesRegex(ValueError, "numeric"):
            production.parse_match_detail(raw)

    def test_independent_parser_rejects_truncated_row(self):
        raw = fixture_html(mid="001").replace('</tr>', '').encode()
        with self.assertRaisesRegex(ValueError, "Truncated"):
            independent.parse(raw, self.item())


if __name__ == "__main__":
    unittest.main()
