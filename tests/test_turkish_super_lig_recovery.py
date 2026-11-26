"""Targeted synthetic recovery tests; no private data or real network."""
from copy import deepcopy
import csv,io
from datetime import date
import unittest
from scripts import recover_turkish_super_lig_sources as r
from scripts import assess_turkish_super_lig_sources as a


def population():
    pairs=[(f'T{i}',f'T{j}') for i in range(18) for j in range(18) if i!=j]
    source=[];fd=[];rss=[]
    for i,(home,away) in enumerate(pairs):
        old='2006-08-04' if i<153 else '2006-03-01';correct=old if i<153 else '2007-03-01'
        source.append(dict(zip(a.HIST_COLUMNS,[old,'2006',home,away,'2-1','2','1','T1','1','3','1','H'])))
        x=dict(home=home,away=away,hg='2',ag='1',date=correct,line=i+2)
        fd.append(x);rss.append(dict(x,date='2007-03-02' if 153<=i<163 else correct))
    text=io.StringIO(newline='');w=csv.DictWriter(text,fieldnames=a.HIST_COLUMNS);w.writeheader();w.writerows(source);raw=text.getvalue().encode()
    hist=r.csv_original(raw);registry=r.recover(hist,fd,rss,[]);registry['source_sha256']=r.c.sha(raw)
    return raw,hist,fd,rss,registry


class RecoveryChecks(unittest.TestCase):
    def test_issue_classes(self):
        self.assertEqual(r.classify(bounded=True,provenance_ok=True,privacy_ok=True,corroborated=True),'RECOVERABLE_SOURCE_ISSUE')
        self.assertEqual(r.classify(bounded=True,provenance_ok=True,privacy_ok=True,corroborated=False),'ISOLATED_QUARANTINE')
        for key in ['bounded','provenance_ok','privacy_ok']:
            args=dict(bounded=True,provenance_ok=True,privacy_ok=True,corroborated=True);args[key]=False
            with self.subTest(key=key):self.assertEqual(r.classify(**args),'SYSTEMIC_BLOCKED')

    def test_recovery_counts_and_original_preserved(self):
        raw,hist,fd,rss,registry=population();before=bytes(raw)
        self.assertEqual(registry['summary'],dict(affected=153,season_pair_score_corroborated=153,derived_date_corrected=143,quarantined=10,unchanged_first_half=153))
        summary,excluded=r.apply_metadata(raw,registry)
        self.assertEqual(summary['2006']['dated_scored'],296);self.assertEqual(len(excluded),10);self.assertEqual(raw,before)
        self.assertNotIn('match_id',repr(registry));self.assertTrue(all(z['football_result_decision'] is None for z in registry['affected_records']))

    def test_disagreements_quarantined_across_sources(self):
        raw,hist,fd,rss,registry=population()
        self.assertEqual(len(r.source_candidates(fd,registry,'2006/2007')),296)
        self.assertEqual(len(r.source_candidates(rss,registry,'2006/2007')),296)
        self.assertEqual(len(r.source_candidates(fd,registry,'2025/2026')),306)
        x=next(z for z in registry['affected_records'] if z['derived_date'] is None)
        self.assertEqual(x['action'],'QUARANTINE_ALL_COMPARED_REPRESENTATIONS')

    def test_wrong_source_or_record_hash_rejected(self):
        raw,hist,fd,rss,registry=population()
        with self.assertRaisesRegex(ValueError,'another original'):r.apply_metadata(raw+b'\n',registry)
        changed=deepcopy(registry);changed['affected_records'][0]['physical_sha256']='bad'
        with self.assertRaisesRegex(ValueError,'record differs'):r.apply_metadata(raw,changed)

    def test_correction_requires_exact_agreement(self):
        raw,hist,fd,rss,registry=population();changed=deepcopy(registry)
        row=next(x for x in changed['affected_records'] if x['derived_date'] is None);row['action']='DERIVED_DATE_CORRECTION';row['derived_date']=row['fd']['date']
        with self.assertRaisesRegex(ValueError,'Unsupported correction'):r.apply_metadata(raw,changed)

    def test_score_mismatch_cannot_drive_identity_or_date_repair(self):
        raw,hist,fd,rss,registry=population();rss[200]['hg']='9'
        with self.assertRaisesRegex(ValueError,'score disagreement'):r.recover(hist,fd,rss,[])

    def test_ambiguous_pair_and_expanded_defect_fail_closed(self):
        raw,hist,fd,rss,registry=population();fd[-1]=fd[0]
        with self.assertRaisesRegex(ValueError,'Ambiguous'):r.recover(hist,fd,rss,[])
        raw,hist,fd,rss,registry=population();rss[0]['date']='2006-08-05'
        with self.assertRaisesRegex(ValueError,'Uncontained'):r.recover(hist,fd,rss,[])

    def test_rsssf_year_comes_from_title_and_heading(self):
        raw='''<TITLE>Turkey 2006/07</TITLE>
Copyright; You are free to copy this document
Round 1
[Aug 4]
Ankaraspor  1-1 Galatasaray
Round 18
[Jan 27]
Galatasaray  2-0 Ankaraspor
Final Table:
Round 1
[Jul 1]
Other  9-9 Club
'''.encode('iso-8859-2')
        rows,notes=r.rsssf_rows(raw,2006);self.assertFalse(notes);self.assertEqual(len(rows),2);self.assertEqual(rows[1]['date'],'2007-01-27')
        with self.assertRaisesRegex(ValueError,'season title'):r.rsssf_rows(raw,2005)

    def test_award_annotation_is_not_a_played_result_decision(self):
        raw='''<TITLE>Turkey 2006/07</TITLE>
You are free to copy this document
Round 1
[Mar 17]
Vestel Manisaspor  awd Sakaryaspor  [awarded 0-3; abandoned at 1-1]
Final Table:
'''.encode('iso-8859-2')
        rows,notes=r.rsssf_rows(raw,2006);self.assertEqual(rows[0]['hg'],'0');self.assertIn('NOT_PLAYED_STATUS_DECISION',rows[0]['kind'])

    def test_direct_empty_padding_and_explicit_annex(self):
        header='Div,Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR\n'
        core='T1,17/03/2007,Manisaspor,Sakaryaspor,0,3,A'
        raw=(header+core+',,Manisaspor,Sakaryaspor,1,1,,,Abandoned\n').encode()
        row=r.direct_rows(raw)[0];self.assertEqual(row['extra_source_columns'][3:5],['1','1']);self.assertIn('ABANDONMENT',row['annex_kind'])
        with self.assertRaisesRegex(ValueError,'shape'):r.direct_rows(raw.replace(b',,Manisaspor,Sakaryaspor,1',b',,Another,Sakaryaspor,1'))
        self.assertEqual(len(r.direct_rows((header+core+',,,,,,,,\n').encode())),1)

    def test_bom_is_handled_without_altering_source(self):
        raw=b'\xef\xbb\xbfDiv,Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR\r\nT1,08/08/2025,A,B,1,0,H\r\n'
        self.assertEqual(a.csv_summary(raw,False)['2025']['dated_scored'],1);self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))

    def test_covid_window_is_explicit_and_bounded(self):
        self.assertEqual(r.turkish_heading('Sun Jul 26 2020',2019)['date'],'2020-07-26')
        with self.assertRaises(ValueError):r.turkish_heading('Mon Jul 27 2020',2019)


if __name__=='__main__':unittest.main()
