"""Dependency-free synthetic Phase 1 checks: no originals or real network."""
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from scripts import collect_turkish_super_lig_sources as c
from scripts import assess_turkish_super_lig_sources as a


def item():
    return dict(path='metadata/notice.txt',url='https://raw.githubusercontent.com/example/test/pin/notice.txt',max_bytes=100,publisher='Synthetic',kind='permission_metadata',licensing='Synthetic test grant',permission_basis='Synthetic',encoding='utf-8-sig')


def plan(i=None):return dict(phase=1,scope='synthetic',items=[i or item()])


class Response:
    status=200
    def __init__(self,i,raw=b'notice',headers=None):self.url=i['url'];self.raw=raw;self.headers=headers or {}
    def __enter__(self):return self
    def __exit__(self,*exc):pass
    def read(self,n):return self.raw[:n]


class Opener:
    def __init__(self,response=None):self.response=response;self.calls=0
    def open(self,*args,**kwargs):
        self.calls+=1
        if isinstance(self.response,Exception):raise self.response
        return self.response


def historical(**changes):
    r=dict(zip(a.HIST_COLUMNS,['2006-08-04','2006','A','B','2-1','2','1','T1','1','3','1','H']));r.update(changes)
    s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=a.HIST_COLUMNS);w.writeheader();w.writerow(r);return s.getvalue().encode()


class TurkishSourceChecks(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory(prefix='turkey-phase1-test-');self.addCleanup(self.temporary.cleanup);self.path=Path(self.temporary.name)

    def test_path_and_symlink_escape(self):
        for path in ['../escape','/tmp/escape','a/../../escape']:
            with self.subTest(path=path),self.assertRaises(ValueError):c.destination(self.path,path)
        (self.path/'link').symlink_to(self.path.parent,target_is_directory=True)
        with self.assertRaises(ValueError):c.destination(self.path,'link/escape')

    def test_invalid_and_duplicate_plan(self):
        for change in [dict(url='http://raw.githubusercontent.com/a'),dict(url='https://example.invalid/a'),dict(url='https://u:p@raw.githubusercontent.com/a'),dict(max_bytes=2000001),dict(kind='fixture'),dict(expected_blob='x')]:
            i=item();i.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):c.validate_plan(plan(i))
        p=plan();p['items']*=2
        with self.assertRaises(ValueError):c.validate_plan(p)
        self.assertEqual(c.validate_plan(plan())['phase'],1)

    def test_exclusive_save(self):
        p=self.path/'a';c.save(p,b'old')
        with self.assertRaises(FileExistsError):c.save(p,b'new')
        self.assertEqual(p.read_bytes(),b'old')

    def test_cache_replay_and_tamper(self):
        i=item();client=Opener(Response(i));r,new=c.acquire(self.path,i,network=True,opener=client)
        self.assertTrue(new);self.assertEqual(client.calls,1);self.assertEqual(r['sha256'],c.sha(b'notice'))
        other=Opener(AssertionError('No network allowed'))
        self.assertEqual(c.acquire(self.path,i,network=True,opener=other),(r,False));self.assertEqual(other.calls,0)
        (self.path/i['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'checksum'):c.acquire(self.path,i,network=True,opener=other)
        self.assertEqual(other.calls,0)

    def test_partial_pair(self):
        i=item();c.save(self.path/i['path'],b'notice');client=Opener()
        with self.assertRaisesRegex(ValueError,'Partial'):c.acquire(self.path,i,network=True,opener=client)
        self.assertEqual(client.calls,0)

    def test_phase_blocker_prevents_network(self):
        c.save(self.path/'BLOCKED.json',c.encode(dict(status='BLOCKED')));client=Opener()
        with self.assertRaisesRegex(RuntimeError,'Phase blocked'):c.acquire(self.path,item(),network=True,opener=client)
        self.assertEqual(client.calls,0)

    def test_access_stop_without_retry(self):
        for mode in ['denial','redirect','retry','too_large','encoding','blob']:
            with self.subTest(mode=mode):
                directory=self.path/mode;i=item();r=Response(i)
                if mode=='denial':client=Opener(PermissionError('HTTP 403'))
                else:
                    if mode=='redirect':r.url='https://example.invalid/redirect'
                    if mode=='retry':r.headers={'Retry-After':'60'}
                    if mode=='too_large':r.raw=b'x'*101
                    if mode=='encoding':r.raw=b'\xff'
                    if mode=='blob':i.update(commit='pin',expected_blob='bad',expected_bytes=6)
                    client=Opener(r)
                with self.assertRaises(Exception):c.acquire(directory,i,network=True,opener=client)
                self.assertEqual(client.calls,1);self.assertTrue(list((directory/'access').glob('*.STOP.json')))
                with self.assertRaisesRegex(RuntimeError,'Prior access'):c.acquire(directory,i,network=True,opener=client)
                self.assertEqual(client.calls,1);self.assertFalse((directory/i['path']).exists())

    def test_permission_required_and_bound(self):
        i=item();i.update(kind='fixture',permission_reference='metadata/grant.txt',permission_sha256=c.sha(b'grant'));client=Opener()
        with self.assertRaisesRegex(ValueError,'Permission'):c.acquire(self.path,i,network=True,opener=client)
        p=self.path/i['permission_reference'];c.save(p,b'changed');c.save(p.with_name(p.name+'.provenance.json'),c.encode(dict(sha256=c.sha(b'grant'))))
        with self.assertRaisesRegex(ValueError,'Permission evidence checksum'):c.acquire(self.path,i,network=True,opener=client)
        self.assertEqual(client.calls,0)

    def test_date_season_blocker_remains(self):
        raw=historical(Date='2006-01-27')
        with self.assertRaisesRegex(ValueError,'Invalid date/team'):a.csv_summary(raw,True)
        self.assertIn(b'2006-01-27',raw)

    def test_csv_contradictions(self):
        for change in [dict(FT='3-1'),dict(result='A'),dict(tier='2'),dict(division='T2'),dict(hgoal=''),dict(totgoal='4')]:
            with self.subTest(change=change),self.assertRaises(ValueError):a.csv_summary(historical(**change),True)
        result=a.csv_summary(historical(),True)
        self.assertEqual(result['2006']['dated_scored'],1);self.assertNotIn('records',result);self.assertNotIn('match_id',repr(result))

    def test_unscored_text_and_invalid_context(self):
        raw='= Turkish Süper Lig 2025/26\n# Matches 2\n▪ 1. Round\nFri Aug 8 2025\nA v B  2-1\nC v D\n'.encode()
        r=a.txt_summary(raw,2025)
        self.assertEqual((r['observations'],r['dated_scored'],r['unscored']),(2,1,1))
        with self.assertRaises(ValueError):a.txt_summary(raw.replace(b'Fri',b'Thu'),2025)
        with self.assertRaises(ValueError):a.txt_summary(raw,2024)

    def test_undated_grid_not_exact_dates(self):
        raw=b'Copyright RSSSF; You are free to copy this document\na |---|1-0|2-0|\n'
        self.assertEqual(a.rsssf_summary(raw,'tur94')['dated_scored_certified'],0)


if __name__=='__main__':unittest.main()
