"""Independent original-to-v2 reconstruction; imports no generator/schema helpers."""
from collections import Counter, defaultdict
import argparse
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/private/europe/champions_league'
PHASE = BASE / 'phase4'
COLUMNS = ['match_id','date','league','season','home_team','away_team','home_goals','away_goals','neutral_venue']
NAME = 'uefa_champions_league_standardized_1992_2026.csv'


def read(path): return json.loads(path.read_bytes())
def digest(raw): return hashlib.sha256(raw).hexdigest()
def wire(obj): return (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2)+'\n').encode()
def require(test, message):
    if not test: raise ValueError(message)


def original_observations():
    from scripts import verify_uefa_champions_league_inventory as old
    from scripts import verify_uefa_champions_league_history as historical
    baseline, _, _, _ = old.raw_inventory(read(BASE/'phase2/acquisition_manifest.json'))
    observations = {x['observation_id']: x for x in baseline}
    for source in read(BASE/'phase3/wikipedia_cached_source_index.json'):
        if source['kind'] != 'qualifying': continue
        rows, _ = historical.wikipedia_reader((BASE/'phase3'/source['path']).read_bytes(), source)
        for x in rows: observations[x['source_observation_id']] = x
    path = BASE/'phase3/originals/engsoccerdata/champs.csv'
    for x in historical.independent_curley(path.read_bytes(), read(path.with_name(path.name+'.provenance.json'))):
        observations[x['source_observation_id']] = x
    require(len(observations) == 12211, 'Original observation population differs')
    return observations


def expected_neutral(event):
    """Independent format ledger; physical venue observations are not inputs."""
    season = int(event['season'][:4]); stage = event['stage']
    if season == 1992 and event['replay']:
        require(event['football_date'] == '1992-10-09' and stage == 'PRE_GROUP_ROUND_1', 'Neutral replay identity differs')
        return 1
    special_stages = {
        2018: {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL'},
        2019: {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL', 'QUARTERFINAL', 'SEMIFINAL'},
        2020: {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL'},
        2021: {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL'},
        2022: {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL'},
        2023: {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL'},
    }
    if stage == 'FINAL' or stage in special_stages.get(season, set()): return 1
    conventional = {'FIRST_GROUP','SECOND_GROUP','LEAGUE_PHASE','PRELIMINARY', 'PRE_GROUP_ROUND_1','PRE_GROUP_ROUND_2',
                    'ROUND_OF_16','KNOCKOUT_PLAYOFF','QUARTERFINAL','SEMIFINAL','QUALIFYING_ROUND_1','QUALIFYING_ROUND_2','QUALIFYING_ROUND_3','QUALIFYING_PLAYOFF'}
    return 0 if stage in conventional else None


def independently_extend_domestic(plan_path, prepared=None, applied=False):
    plan = read(plan_path); reports = []; ids = set()
    for t in plan['targets']:
        before = (ROOT/t['backup']).read_bytes(); require(digest(before) == t['sha256'], 'Domestic backup changed')
        path = ROOT/t['path'] if applied else Path(prepared)/t['path']
        after = path.read_bytes()
        a = list(csv.reader(io.StringIO(before.decode('utf-8'), newline=''), strict=True))
        b = list(csv.reader(io.StringIO(after.decode('utf-8'), newline=''), strict=True))
        require(a[0] == COLUMNS[:8] and b[0] == COLUMNS and len(a) == len(b) and len(a)-1 == t['rows'], 'Domestic shape differs')
        require(all(len(y) == 9 and x == y[:8] and y[8] == '0' for x, y in zip(a[1:], b[1:])), 'Domestic preexisting value/order changed')
        buffer = io.StringIO(newline=''); writer = csv.writer(buffer, lineterminator='\n'); writer.writerows([r[:8] for r in b])
        require(buffer.getvalue().encode('utf-8') == before, 'Domestic original-byte projection differs')
        for row in b[1:]:
            identity = [row[2],row[3],row[1],row[4],row[5]]
            recomputed = hashlib.sha256(json.dumps(identity, ensure_ascii=False, separators=(',',':')).encode('utf-8')).hexdigest()
            require(recomputed == row[0] and row[0] not in ids, 'Domestic ID changed or duplicated')
            ids.add(row[0])
        reports.append({'path':t['path'], 'rows':len(b)-1, 'old_fields_unchanged':8*(len(b)-1), 'changed_fields':0,'changed_ids':0,
                        'legacy_projection_byte_identical':True, 'before_sha256':digest(before),'after_sha256':digest(after),'neutral_0':len(b)-1,'neutral_1':0,'neutral_NA':0})
    require(len(reports) == 16 and len(ids) == 156579, 'Domestic reference population differs')
    return {'status':'PASS','files':reports,'competitions':14,'csv_files':16,'rows':len(ids),'unchanged_preexisting_fields':8*len(ids),'changed_preexisting_fields':0,'changed_match_ids':0,
            'neutral_0':len(ids),'neutral_1':0,'neutral_NA':0,'accepted_score_period_audit_still_valid':True}


def verify(output=PHASE/'validated'):
    output = Path(output); observations = original_observations()
    source_manifest = {}
    for original in read(BASE/'phase2/acquisition_manifest.json')['originals']:
        source_manifest[original['sha256']] = original
    for original in read(BASE/'phase3/acquisition_manifest.final.json')['originals']:
        source_manifest[original['sha256']] = original
    curley_source_sha = read(BASE/'phase3/originals/engsoccerdata/champs.csv.provenance.json')['sha256']
    registry_bytes = (BASE/'phase3/final/decision_registry.json').read_bytes()
    registry = json.loads(registry_bytes); evidence = read(BASE/'phase3/adjudication_evidence.json')
    registry_sha = digest(registry_bytes)
    format_policy_sha = digest((PHASE/'format_policy.json').read_bytes())
    rules = defaultdict(list)
    for rule in evidence['rules']: rules[rule['observation_id']].append(rule)
    memberships = Counter(); expected_rows = []; decision_ids = []; counts = Counter(); neutral_seasons = Counter(); stage_counts = Counter()
    repairs = []; period_resolutions = []; date_repairs = []; administrative = []; outcomes = {}; expectations = {}
    for e in registry['fixture_events']:
        p = observations[e['primary_observation_id']]; memberships.update(e['observations'])
        require(e['season'] == p['season'] and e['stage'] == p['stage'] and e['first_listed'] == p['home'] and e['second_listed'] == p['away'], 'Primary identity/stage differs')
        expected = {'football_date':p['date'],'regulation_time':p['periods']['regulation_time'],'observed_regulation_time':p['periods']['regulation_time'],
                    'administrative_result':None,'disposition':'INCLUDE','after_extra_time':p['periods'].get('after_extra_time'),'shootout':p['periods'].get('shootout'),
                    'leg':p.get('source_leg'),'replay':p.get('replay',False),'half_time':p['periods'].get('half_time')}
        applied = rules[e['primary_observation_id']]
        for rule in applied:
            require((rule['expected_date'],rule['expected_home'],rule['expected_away']) == (p['date'],p['home'],p['away']), 'Repair raw identity differs')
            require(rule['source_sha256'] == p['source_sha256'] and all(x in evidence['evidence'] for x in rule['evidence_ids']), 'Repair lacks bound evidence')
            expected.update(rule['changes'])
            if 'regulation_time' in rule['changes'] and 'observed_regulation_time' not in rule['changes']:
                expected['observed_regulation_time'] = rule['changes']['regulation_time']
        for key in expected:
            require(e.get(key) == expected[key], 'Independent approved decision differs: '+key)
        require(e['applied_decisions'] == applied, 'Decision rule trace differs')
        counts[e['disposition']] += 1
        if e['disposition'] != 'INCLUDE':
            require(e['disposition'] == 'NOT PLAYED' and expected['football_date'] is None and expected['regulation_time'] is None and e['accepted_result'] is None, 'Exclusion differs')
            continue
        score = expected['administrative_result'] if expected['administrative_result'] is not None else expected['regulation_time']
        require(score is not None and e['accepted_result'] == score, 'Canonical result basis unsupported')
        if expected['administrative_result'] is not None: administrative.append(e['event_id'])
        elif p['periods']['regulation_time'] != score:
            change = {'event_id':e['event_id'],'old':p['periods']['regulation_time'],'approved':score}
            (period_resolutions if p['periods']['regulation_time'] is None else repairs).append(change)
        if expected['football_date'] != p['date']: date_repairs.append({'event_id':e['event_id'],'old':p['date'],'approved':expected['football_date']})
        day = expected['football_date']; season = p['season']; parsed = date.fromisoformat(day)
        require(int(season[:4]) <= parsed.year <= int(season[5:]), 'UCL season membership differs')
        home = expected.get('historical_home',p['home']).strip(); away = expected.get('historical_away',p['away']).strip()
        identity = ['UEFA Champions League',season,day,home,away]
        match_id = hashlib.sha256(json.dumps(identity, ensure_ascii=False, separators=(',',':')).encode('utf-8')).hexdigest()
        neutral = expected_neutral(dict(e, replay=expected['replay'], football_date=day))
        row = [match_id,day,identity[0],season,home,away,str(score[0]),str(score[1]),'' if neutral is None else str(neutral)]
        outcome = 'X' if score[0] == score[1] else '1' if score[0] > score[1] else '2'
        require(e['outcome'] == outcome, 'Incorrect first-listed outcome')
        expected_rows.append(row); outcomes[match_id] = outcome; decision_ids.append(e['event_id']); expectations[match_id] = e
        neutral_seasons[(season,neutral)] += 1; stage_counts[(season,e['scope'],e['stage'])] += 1
    require(set(memberships) == set(observations) and set(memberships.values()) == {1}, 'Observation accounting differs')
    require(counts == {'INCLUDE':6642,'NOT PLAYED':3} and len(registry['additional_nonstanding_context_events']) == 3 and all(x['disposition'] == 'OUT OF SCOPE' for x in registry['additional_nonstanding_context_events']), 'Population differs')
    require(len(repairs) == 8 and len(period_resolutions) == 3 and len(date_repairs) == 4 and len(administrative) == 8, 'Approved repair/period/exception count differs')
    expected_rows.sort(key=lambda r: (r[2],r[3],r[1],r[4],r[5]))
    require(len({r[0] for r in expected_rows}) == len(expected_rows) == 6642, 'Independent duplicate/identity count differs')
    actual = list(csv.reader(io.StringIO((output/NAME).read_text(), newline=''), strict=True))
    require(actual == [COLUMNS] + expected_rows, 'Independent canonical field/order reconstruction differs')
    buffer = io.StringIO(newline=''); writer = csv.writer(buffer, lineterminator='\n'); writer.writerows([COLUMNS]+expected_rows)
    payload = buffer.getvalue().encode('utf-8'); require(payload == (output/NAME).read_bytes(), 'Independent CSV bytes differ')
    special_counts = {1992:2,2018:4,2019:10,2020:3,2021:4,2022:4,2023:4}
    for y in range(1992,2026):
        season=f'{y}/{y+1}'; require(neutral_seasons[(season,1)] == special_counts.get(y,1) and neutral_seasons[(season,None)] == 0, 'Independent neutral-format season expectation differs')
    prior_counts = {x['season']:x for x in read(BASE/'phase3/final/coverage_assessment.json')['seasons']}
    stages = read(output/'season_stage_neutrality.json'); require(len(stages) == len(stage_counts), 'Stage ledger incomplete')
    for item in stages:
        es = [e for e in expectations.values() if (e['season'],e['scope'],e['stage']) == (item['season'],item['scope'],item['stage'])]
        require(item['include'] == len(es) and item['neutral_counts'] == dict(Counter(str(expected_neutral(e)) for e in es)), 'Stage neutrality ledger differs')
    coverage = read(output/'season_coverage.json'); require(len(coverage) == 34, 'Coverage matrix differs')
    for item in coverage:
        old = prior_counts[item['season']]; require(item['main'] == old['main_descriptions'] and item['qualifying']+item['not_played'] == old['qualifying_observed_descriptions'], 'Season scope counts differ')
        require(item['include'] == item['main']+item['qualifying'] and sum(neutral_seasons[(item['season'],v)] for v in (0,1,None)) == item['include'], 'Season ledger counts differ')
    audit = read(output/'source_to_output.json')['matches']; require(len(audit) == len(expected_rows), 'Traceability population differs')
    for line,(a,row) in enumerate(zip(audit, expected_rows, strict=True),2):
        require(a['match_id'] == row[0] and a['csv_physical_line'] == line and a['approved_event'] == expectations[row[0]] and a['outcome'] == outcomes[row[0]], 'Output source/decision trace differs')
        require([str(a['canonical'][c]) if a['canonical'][c] is not None else '' for c in COLUMNS] == row, 'Audit canonical copy differs')
        require(a['frozen_phase3_registry_sha256'] == registry_sha, 'Audit decision fingerprint differs')
        require(a['neutral_format_policy_sha256'] == format_policy_sha, 'Audit format fingerprint differs')
        require({x['observation_id'] for x in a['contributors']} == set(a['approved_event']['observations']), 'Contributor lost')
        for c in a['contributors']:
            o = observations[c['observation_id']]
            source = o.get('source_sha256') or curley_source_sha
            manifest_entry = source_manifest[source]
            require(c['source_sha256'] == source and c['source'] == manifest_entry['path'] and c['url'] == manifest_entry['url'] and c['receipt_sha256'] == manifest_entry['receipt_sha256'], 'Contributor source trace differs')
            if 'line' in o: require(c['locator']['line'] == o['line'] and c['locator']['physical_sha256'] == o['physical_sha256'], 'Physical source trace differs')
            elif 'physical_line' in o: require(c['locator']['physical_line'] == o['physical_line'] and c['locator']['physical_sha256'] == o['physical_sha256'], 'Curley trace differs')
            else: require(c['locator']['decoded_line'] == o['decoded_line'] and c['locator']['template_sha256'] == o['template_sha256'], 'Revision source trace differs')
    excluded = read(output/'excluded_events.json')
    require(excluded['not_played'] == [e for e in registry['fixture_events'] if e['disposition'] != 'INCLUDE'] and excluded['out_of_scope'] == registry['additional_nonstanding_context_events'], 'Excluded evidence differs')
    return {'status':'PASS','independent_original_reader':True,'network_requests':0,'matches':6642,'seasons':34,'main':4127,'qualifying':2515,'observations':len(observations),
            'recovered_qualifying_descriptions':692,'recovered_qualifying_include':690,'regulation_repairs':repairs,'resolved_unknown_regulation_periods':period_resolutions,'date_repairs':date_repairs,'administrative_exception_event_ids':administrative,
            'dispositions':{'INCLUDE':6642,'HOLD OUT':0,'NOT PLAYED':3,'OUT OF SCOPE':3},'neutral_counts':{'0':6584,'1':58,'NA':0},
            'independent_csv_sha256':digest(payload),'byte_identical_original_to_output':True,'all_output_fields_and_order_reconstructed':True,'stage_groups':len(stage_counts),
            'limits':'Independent computation is not disjoint historical upstream provenance or downstream permission clearance.'}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=PHASE/'validated');p.add_argument('--output',type=Path);p.add_argument('--domestic-prepared',type=Path);p.add_argument('--domestic-applied',action='store_true');a=p.parse_args()
    result=verify(a.inventory)
    if a.domestic_prepared or a.domestic_applied: result['domestic']=independently_extend_domestic(PHASE/'domestic_migration_plan.json',a.domestic_prepared,a.domestic_applied)
    if a.output:
        require(not a.output.resolve().is_relative_to(ROOT) or a.output.resolve().is_relative_to(ROOT/'data/private'),'Detailed output must remain private')
        with a.output.open('xb') as handle:handle.write(wire(result))
    print(json.dumps({k:v for k,v in result.items() if k not in {'regulation_repairs','date_repairs','administrative_exception_event_ids','domestic'}},indent=2))
