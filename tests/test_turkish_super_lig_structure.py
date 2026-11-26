"""Synthetic structural checks and adversarial inventory reconciliation."""
import unittest
from copy import deepcopy
from scripts import inventory_turkish_super_lig as p
from scripts import validate_turkish_super_lig_structure as v


def rec(raw,kind='rsssf',season='1992/1993'):
    return dict(root_path='synthetic/'+kind,sha256=p.c.sha(raw),bytes=len(raw),kind=kind,season=season,top_span=[1,len(raw.splitlines())])


def row(sid,source,home,away,day='2025-08-08',hg='2',ag='1',stage='REGULAR_SEASON'):
    r=p.observation(2025,home,away,hg,ag);r.update(source_id=sid,source=source,date=day,stage=stage);return r


class StructureChecks(unittest.TestCase):
    def test_split_round_heading_preserved_in_both_parsers(self):
        raw=b'<TITLE>Turkey 1992/93</TITLE>\n1. Round (23 August 1992)\nA - B : 1-0\n12. Round\n(22 November 1992)\nC - D : 2-0\n'
        r=rec(raw);out,_,_=p.parse_rsssf(raw,r);ind,_=v.parse_rsssf(raw,r)
        self.assertEqual([r['round'] for r in out],[1,12]);self.assertEqual([r['round'] for r in ind],[1,12]);self.assertTrue(all(r['date'] is None for r in out));self.assertEqual(out[1]['nominal_date_heading'],'22 November 1992')

    def test_undated_grid_cell_provenance(self):
        cols=['koc','bes','bur','gal','fen','tra','kar','gen','alt','gaz','sar','zey','kay','ank','sam','krb'];lines=['<TITLE>Turkey 1993/94</TITLE>']
        lines+=[' '.join(c[i] for c in cols) for i in range(3)]
        lines += [h+' |'+'|'.join('---' if h==a else '0-0' for a in cols)+'|' for h in cols]
        raw=('\n'.join(lines)+'\n').encode();r=rec(raw,season='1993/1994');a,_,_=p.parse_rsssf(raw,r);b,_=v.parse_rsssf(raw,r)
        self.assertEqual(len(a),240);self.assertEqual({x['source_id'] for x in a},{x['source_id'] for x in b});self.assertEqual(len({x['source_id'] for x in a}),240);self.assertTrue(all(x['date'] is None for x in a));self.assertEqual(len({x['physical_sha256'] for x in a}),16)

    def test_cancelled_award_has_no_invented_play_date(self):
        raw=b'<TITLE>Turkey 2022/23</TITLE>\nRound 24\n[Mar 6]\nA  2-1 B\n[cancelled matches]\nC  awd D  [awarded 3-0]\nE bye\nFinal Table:\n'
        r=rec(raw,season='2022/2023');a,_,notes=p.parse_rsssf(raw,r);b,_=v.parse_rsssf(raw,r)
        self.assertEqual(len(a),2);self.assertEqual(a[1]['hg'],'3');self.assertIsNone(a[1]['date']);self.assertIsNone(b[1]['date']);self.assertTrue(any(x['kind']=='BYE_NOT_FIXTURE' for x in notes))

    def test_abandonment_and_replay_stay_distinct(self):
        raw=b'<TITLE>Turkey 2005/06</TITLE>\nRound 30\n[Apr 15]\nA  abd B  [abandoned at 1-0]\n[Apr 16]\nA  3-0 B  [replay]\nFinal Table:\n'
        r=rec(raw,season='2005/2006');a,_,_=p.parse_rsssf(raw,r);self.assertEqual(len(a),2);self.assertIsNone(a[0]['hg']);self.assertNotEqual(a[0]['source_id'],a[1]['source_id']);self.assertNotEqual(a[0]['date'],a[1]['date'])

    def test_narrative_score_not_fixture(self):
        raw=b'<TITLE>Turkey 2022/23</TITLE>\nRound 1\n[Aug 5]\nA  2-1 B\nNB: clubs withdrew\n    awarded 0-3 losses against them\n\nRound 2\n[Aug 12]\nB  0-0 A\nFinal Table:\n'
        a,_,_=p.parse_rsssf(raw,rec(raw,season='2022/2023'));b,_=v.parse_rsssf(raw,rec(raw,season='2022/2023'));self.assertEqual(len(a),2);self.assertEqual(len(b),2)

    def test_leap_day_and_covid_date_resolution(self):
        for season,title,heading in [('2023/2024','2023/24','Thu Feb 29'),('2019/2020','2019/20','Sun Jul 26 2020')]:
            raw=f'= Turkish Süper Lig {title}\n▪ Matchday 1\n{heading}\nA v B  1-0\n'.encode();r=rec(raw,'txt',season);a,_,_=p.parse_txt(raw,r);b,_=v.parse_txt(raw,r);self.assertEqual(a[0]['date'],b[0]['date'])

    def test_wrong_txt_title_rejected(self):
        raw='= Turkish Süper Lig 2024/25\n▪ Matchday 1\nFri Aug 8 2025\nA v B  1-0\n'.encode();r=rec(raw,'txt','2025/2026')
        with self.assertRaises(ValueError):p.parse_txt(raw,r)
        with self.assertRaises(AssertionError):v.parse_txt(raw,r)

    def test_single_space_rsssf_fixture_not_silently_lost(self):
        raw=b'<TITLE>Turkey 2005/06</TITLE>\nRound 24\n[Mar 4]\nAlpha Club 1-2 Beta Club\nFinal Table:\n';r=rec(raw,season='2005/2006');a,_,_=p.parse_rsssf(raw,r);b,_=v.parse_rsssf(raw,r);self.assertEqual(len(a),1);self.assertEqual(a[0]['away'],'Beta Club');self.assertEqual(len(b),1)

    def test_raw_quarantine_is_not_dropped_or_repaired(self):
        raw=b'Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result\n2006-01-27,2006,A,B,1-1,1,1,T1,1,2,0,D\n';r=rec(raw,'historical_csv','2006/2007');physical=raw.splitlines(keepends=True);fields=dict(zip(raw.splitlines()[0].decode().split(','),raw.splitlines()[1].decode().split(',')))
        rule=dict(source_line=2,original_fields=fields,physical_sha256=p.c.sha(physical[1]),action='QUARANTINE_ALL_COMPARED_REPRESENTATIONS',derived_date=None,fd=dict(date='2007-01-27'),rsssf=dict(date='2007-01-28'))
        a,_,_=p.parse_csv(raw,r,dict(affected_records=[rule]));b,_=v.parse_csv(raw,r,{2:rule});self.assertEqual(len(a),1);self.assertTrue(a[0]['quarantined']);self.assertIsNone(a[0]['date']);self.assertEqual(a[0]['reported_date'],'2006-01-27');self.assertTrue(b[0]['quarantined'])
        bad=deepcopy(rule);bad['physical_sha256']='wrong'
        with self.assertRaises(ValueError):p.parse_csv(raw,r,dict(affected_records=[bad]))

    def test_schedule_difference_not_scored_date_quarantine(self):
        anchor=[row('a'+str(i),'x/T1.csv','A','B',f'2025-08-{8+i:02d}') for i in range(2)]
        # Use distinct pairings with repeated names for coeval proof.
        anchors=[row('h1','x/T1.csv','A','B'),row('h2','x/T1.csv','B','A','2025-08-09'),row('h3','x/T1.csv','A','B','2025-08-10')]
        secondary=[row('s1','y/file','X','Y'),row('s2','y/file','Y','X','2025-08-09'),row('s3','y/file','X','Y','2025-08-10')]
        mapping,_=p.correspond(anchors,secondary);self.assertEqual(mapping,{'X':'A','Y':'B'})
        # Direct same-label evidence requires two games per side; complete small
        # 3-team source gives each name multiple independent fixture witnesses.
        hs=[];ss=[];i=0
        for h in ['A','B','C']:
            for a in ['A','B','C']:
                if h==a:continue
                d=f'2025-08-{8+i:02d}';hs.append(row('h'+str(i),'x/T1.csv',h,a,d));ss.append(row('s'+str(i),'y/file',h,a,d));i+=1
        ss[-1]['date']='2025-09-01';ss[-1]['hg']=ss[-1]['ag']=None
        events,_=p.reconcile(hs+ss);e=next(e for e in events if 's5' in e['source_ids']);self.assertEqual(e['issues'],['SCHEDULE_DATE_DIFFERENCE']);self.assertFalse(e['quarantined'])
        ss[-1]['hg']='2';ss[-1]['ag']='1';events,_=p.reconcile(hs+ss);e=next(e for e in events if 's5' in e['source_ids']);self.assertIn('DATE_CONFLICT',e['issues']);self.assertTrue(e['quarantined'])

    def test_stages_never_collapse(self):
        rows=[row('reg','x/T1.csv','A','B'),row('play','x/T1.csv','A','B','2025-08-08',stage='CHAMPIONSHIP_PLAYOFF')];events,_=p.reconcile(rows);self.assertEqual(len(events),2)

    def test_duplicate_source_observation_retained_for_review(self):
        a=row('one','x/T1.csv','A','B');b=deepcopy(a);b['source_id']='two';events,_=p.reconcile([a,b]);self.assertEqual(len(events),2);self.assertEqual(sum(len(e['source_ids']) for e in events),2)


if __name__=='__main__':unittest.main()
