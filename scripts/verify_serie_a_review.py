"""Read-only consistency checks for manually recorded Serie A external evidence.

Run: PYTHONPATH=src python3 -m scripts.verify_serie_a_review
Never fetches pages, certifies external truth, applies corrections or writes data.
"""
from collections import Counter, defaultdict
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path

from scripts.validate_serie_a import PRIVATE, ROOT, build, historical, football_txt

FULL_ACCESS = {'FULL_MATCH_PAGE', 'FULL_RESULTS_PAGE', 'FULL_REPORT'}
FACTS = ('date', 'home_team', 'away_team', 'home_goals', 'away_goals')


def digest(content):
    return hashlib.sha256(content).hexdigest()


def bound_facts(directory, binding):
    """Verify a physical source line and exact raw values before reading facts."""
    path = directory / binding['source_file']
    if not path.resolve().is_relative_to(directory.resolve()):
        raise ValueError('Source outside private directory')
    content = path.read_bytes()
    if digest(content) != binding['source_sha256']:
        raise ValueError('Source checksum changed')
    line = binding['source_row']
    if path.suffix == '.csv':
        reader = csv.DictReader(io.StringIO(content.decode('utf-8-sig')), strict=True)
        row = next((r for r in reader if reader.line_num == line), None)
        if row is None or row != binding['original_fields']:
            raise ValueError('Source row/fields changed')
        return dict(date=row['Date'], home_team=row['home'], away_team=row['visitor'],
                    home_goals=int(row['hgoal']), away_goals=int(row['vgoal']))
    if path.suffix != '.txt' or not 1 <= line <= len(content.decode('utf-8-sig').splitlines()):
        raise ValueError('Unsupported/absent source line')
    original = {'line': content.decode('utf-8-sig').splitlines()[line-1]}
    if original != binding['original_fields']:
        raise ValueError('Source TXT line changed')
    matches, issues = football_txt(path)
    if issues:
        raise ValueError('TXT parsing issues')
    rows = [r for r in matches if r['source_row'] == line]
    if len(rows) != 1:
        raise ValueError('TXT match absent')
    r = rows[0]
    return dict(date=r['date'], home_team=r['home'], away_team=r['away'],
                home_goals=int(r['hg']), away_goals=int(r['ag']))


def check_samples(samples, minimum=5):
    """Check transcriptions and quotas; discrepancies are retained, not hidden."""
    ids, bindings = set(), set()
    decades, access = Counter(), Counter()
    discrepancies = {}
    for sample in samples:
        ident = sample['sample_id']
        key = (sample['source']['source_file'], sample['source']['source_row'])
        if ident in ids or key in bindings:
            raise ValueError('Duplicate sample or fixture binding')
        ids.add(ident); bindings.add(key)
        observed = sample['observed']
        day = date.fromisoformat(observed['date'])
        if observed['competition'] != 'Serie A' or observed['regular_season'] is not True:
            raise ValueError('Wrong competition or stage')
        if not sample['reference_url'].startswith('https://') or not sample['evidence_note']:
            raise ValueError('Missing reference/evidence')
        for side in ('home_team', 'away_team'):
            if sample['team_identity_mapping'].get(observed[side]) != sample[side]:
                raise ValueError('Unexplained team identity/orientation')
        differences = [k for k in ('date','home_goals','away_goals') if sample[k] != observed[k]]
        expected = 'DISCREPANCY' if differences else 'AGREES'
        if sample['status'] != expected:
            raise ValueError('Discrepancy concealed or invented')
        if differences:
            discrepancies[ident] = differences
        kind = sample['access']
        if kind in FULL_ACCESS:
            decades[(day.year // 10)*10] += 1
        elif kind != 'INDEXED_ONLY':
            raise ValueError('Unknown evidence access')
        access[kind] += 1
    if any(decades[d] < minimum for d in (1990,2000,2010,2020)):
        raise ValueError('Insufficient full-page calendar-decade coverage')
    return dict(decades= dict(sorted(decades.items())), access=dict(access), discrepancies=discrepancies)


def check_corrections(directory, corrections, samples):
    by_id = {s['sample_id']:s for s in samples}
    wanted = {s['sample_id'] for s in samples if s['status']=='DISCREPANCY'}
    seen, correction_ids, bindings = set(), set(), set()
    for correction in corrections:
        sample_id = correction['sample_id']
        if sample_id not in wanted or sample_id in seen:
            raise ValueError('Correction without unique discrepancy')
        seen.add(sample_id)
        sample = by_id[sample_id]
        if correction['source'] != sample['source']:
            raise ValueError('Correction binding changed')
        key = (correction['source']['source_file'],correction['source']['source_row'])
        if correction['correction_id'] in correction_ids or key in bindings:
            raise ValueError('Duplicate correction')
        correction_ids.add(correction['correction_id']);bindings.add(key)
        facts = bound_facts(directory, correction['source'])
        if any(facts[k] != sample[k] for k in FACTS):
            raise ValueError('Correction/source facts changed')
        if correction['applied'] is not False or correction['status'] != 'VERIFIED_PENDING_STANDARDIZATION':
            raise ValueError('Review cannot apply corrections')
        replacement = correction['replacements']
        # This review established date discrepancies only. Scores/names cannot change.
        if replacement != {'Date':sample['observed']['date']} or replacement['Date']==facts['date']:
            raise ValueError('Unapproved correction scope')
        date.fromisoformat(replacement['Date'])
        if sample['home_goals']!=sample['observed']['home_goals'] or sample['away_goals']!=sample['observed']['away_goals']:
            raise ValueError('Unresolved score discrepancy')
        if not correction['evidence'] or not any(e['access'] in FULL_ACCESS for e in correction['evidence']):
            raise ValueError('No full-page correction evidence')
    if seen != wanted:
        raise ValueError('Missing correction for recorded discrepancy')


def check_policy(directory, policy, corrections, expected_cases=7):
    if policy['unlisted_training_suitability'] != 'UNRESOLVED':
        raise ValueError('Unlisted eligibility assumed')
    cases = policy['known_match_cases']
    if len(cases) != expected_cases or len({c['case_id'] for c in cases}) != len(cases):
        raise ValueError('Missing/duplicate exceptional cases')
    corr = {c['correction_id']:c for c in corrections}
    seen = set()
    decisions = Counter()
    for case in cases:
        facts = bound_facts(directory, case['source'])
        key = (case['source']['source_file'],case['source']['source_row'])
        if key in seen: raise ValueError('Duplicate exceptional fixture')
        seen.add(key)
        if not case['evidence'] or not case['training_reason']:
            raise ValueError('Unsupported exception decision')
        expected = {
            'COMPLETED_REPLAY_AFTER_ABANDONMENT':'EXCLUDED',
            'UNPLAYED_ADMINISTRATIVE_AWARD':'EXCLUDED',
            'FIRST_PLAYED_AFTER_OVERTURNED_AWARD':'ELIGIBLE',
            'INTERRUPTED_THEN_RESUMED_AND_COMPLETED':'UNRESOLVED',
        }.get(case['classification'])
        if expected is None or case['training_suitability'] != expected:
            raise ValueError('Decision inconsistent with recorded policy')
        if expected=='ELIGIBLE' and (case['original_on_field_event']['completed'] is not True or case['actual_playing_or_completion_date'] is None):
            raise ValueError('Eligibility without completed on-field evidence')
        if case['classification']=='UNPLAYED_ADMINISTRATIVE_AWARD' and (case['actual_playing_or_completion_date'] is not None or case['original_on_field_event']['score'] is not None):
            raise ValueError('Invented playing date/score for unplayed award')
        if f"{facts['home_goals']}-{facts['away_goals']}" != case['official_final_result']:
            raise ValueError('Exception final score differs from source')
        final_date = facts['date']
        if case['source_correction_required']:
            correction = corr.get(case['correction_id'])
            if correction is None or correction['source'] != case['source']:
                raise ValueError('Missing bound exception correction')
            final_date = correction['replacements']['Date']
        if final_date != case['official_final_date']:
            raise ValueError('Exception final date unresolved')
        decisions[case['training_suitability']] += 1
    return dict(decisions)


def date_collisions(records):
    """Candidate flags only; never infer real-world corrections from collisions."""
    entries = defaultdict(list)
    for r in records:
        for side in ('home','away'):
            entries[(r['date'],r[side])].append(r['source_row'])
    return [dict(date=d,team=t,source_rows=lines) for (d,t),lines in sorted(entries.items()) if len(lines)>1]


def review():
    directory = PRIVATE/'verification'
    read = lambda name: json.loads((directory/name).read_text())
    manifest = read('review_manifest.json')
    for name, sha in manifest['files'].items():
        if digest((directory/name).read_bytes()) != sha:
            raise ValueError('Recorded review artifact changed: '+name)
    if digest(Path(__file__).read_bytes()) != manifest['checker_sha256']:
        raise ValueError('Review checker revision changed')
    protected = read('protected_before.json')
    for name, sha in protected.items():
        if digest((ROOT/name).read_bytes()) != sha:
            raise ValueError('Protected file changed: '+name)
    outputs, seasons = build()
    for name, content in outputs.items():
        if (PRIVATE/name).read_bytes() != content:
            raise ValueError('Structural audit no longer reproducible: '+name)
    if len(seasons)!=36 or sum(s['matches'] for s in seasons)!=12644 or any(s['status']!='PASS' for s in seasons):
        raise ValueError('Historical source coverage changed')
    main = read('independent_verification.json')['matches']
    supplement = read('supplementary_verification.json')['matches']
    main_summary = check_samples(main)
    samples = main+supplement
    summary = check_samples(samples)
    selection = read('sample_selection.json')
    if selection != [dict(sample_id=s['sample_id'],source=s['source']) for s in main]:
        raise ValueError('Main sample selection replaced')
    for sample in samples:
        facts = bound_facts(PRIVATE, sample['source'])
        if any(facts[k]!=sample[k] for k in FACTS):
            raise ValueError('Sample differs from original')
    corrections = read('verified_corrections.json')['corrections']
    check_corrections(PRIVATE,corrections,samples)
    decisions = check_policy(PRIVATE,read('exception_policy.json'),corrections)
    rows = historical(PRIVATE/'jalapic/data-raw/italy.csv')[0]
    txt = football_txt(PRIVATE/'openfootball/2025-26/1-seriea.txt')[0]
    before = date_collisions(rows+txt)
    dates = {c['source']['source_row']:c['replacements']['Date'] for c in corrections}
    # Simulation exists only in memory: no standardized or corrected data are saved.
    proposed = [dict(r,date=dates.get(r['source_row'],r['date'])) for r in rows]+txt
    after = date_collisions(proposed)
    if after:
        raise ValueError('Unresolved same-team/date collision candidates')
    return dict(records=12644,seasons=36,protected_files_unchanged=len(protected),main_sample=main_summary,
                combined_sample=summary,comparisons=len(samples),exception_decisions=decisions,
                proposed_date_corrections=len(corrections),corrections_applied=0,
                original_same_team_date_collision_groups=len(before),proposed_collision_groups=len(after))


if __name__ == '__main__':
    print(json.dumps(review(),indent=2))
