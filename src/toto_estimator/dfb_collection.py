"""Offline-first Bundesliga inventory, export ingestion and season acceptance gates.

A displayed numeric score is never automatically certified final. Status evidence
is bound to the source response checksum and source match ID. No predictor imports.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re

import pandas as pd

from .data import validate_historical_data
from .validation import exact_integer
from .dfb_html import _Tree, _one, canonical_season, parse_dfb_matchday
from .dfb_transport import digest

STATUSES = {'finished', 'awarded', 'scheduled', 'postponed', 'live', 'abandoned', 'cancelled', 'unknown'}


def season_format(start):
    if not isinstance(start, int) or not 1990 <= start <= 2026:
        raise ValueError('Supported season starts: 1990 through 2026')
    teams = 20 if start == 1991 else 18
    return dict(season=f'{start}/{start+1}', teams=teams, rounds=2*(teams-1),
                matches=teams*(teams-1), ongoing=start==2026)


def inventory_from_html(html):
    """Use actual advertised slugs, never guess historical season URL values."""
    seed = parse_dfb_matchday(html)
    tree = _Tree(); tree.feed(html); tree.close()
    select = _one((n for n in tree.root.walk() if n.tag=='select' and n.attrs.get('name')=='season_id'), 'season select')
    slugs = {}
    for option in select.walk():
        if option.tag != 'option':
            continue
        slug = option.attrs.get('value') or ''
        if not re.fullmatch(r'\d{4}-\d{2,4}', slug):
            continue
        season = canonical_season(slug)
        if season in slugs and slugs[season] != slug:
            raise ValueError('Ambiguous season slugs')
        slugs[season] = slug
    seasons = []
    for start in range(1990,2027):
        fmt = season_format(start); slug = slugs.get(fmt['season'])
        fmt['slug'] = slug
        fmt['urls'] = [f'https://datencenter.dfb.de/de/competitions/bundesliga/seasons/{slug}/matchday/{day}'
                       if slug else None for day in range(1,fmt['rounds']+1)]
        seasons.append(fmt)
    return dict(seed_url=seed.source_url, seed_sha256=digest(html.encode('utf-8')),
                scope='Expected regular-season inventory; not an acquisition/completeness claim', seasons=seasons)


def ingest_exports(cache, manifest_path, *, allowed_urls=None):
    """Import immutable local HTML with provenance; no claim that samples are exports."""
    manifest_path = Path(manifest_path).resolve()
    manifest = json.loads(manifest_path.read_text())
    pages = manifest['pages']
    seen = set()
    skipped = []
    for item in pages:
        url = item['url']
        if allowed_urls is not None and url not in allowed_urls:
            skipped.append(url)
            continue
        if url in seen:
            raise ValueError('Repeated export URL; explicitly review snapshot versions first')
        seen.add(url)
        path = (manifest_path.parent / item['path']).resolve()
        # Export references must stay in the enclosing private Germany tree.
        boundary = next((p for p in (manifest_path.parent, *manifest_path.parents)
                         if p.name == 'germany'), manifest_path.parent)
        if not path.is_relative_to(boundary):
            raise ValueError('Export path escapes private export boundary')
        content = path.read_bytes()
        if digest(content) != item['sha256']:
            raise ValueError('Export checksum mismatch')
        if not item.get('retrieved_at') or not item.get('access_basis') or not item.get('evidence_reference'):
            raise ValueError('Export provenance is incomplete')
        result = parse_dfb_matchday(content.decode('utf-8'))
        if result.source_url != url:
            raise ValueError('Export URL and canonical URL differ')
        cache.store(url, content, retrieved_at=item['retrieved_at'], basis=item['access_basis'],
                    reference=item['evidence_reference'])
    summary = dict(imported_pages=len(seen), skipped_out_of_scope=skipped,
                   manifest_sha256=digest(manifest_path.read_bytes()))
    cache.event(action='exports_ingested', **summary)
    return summary


def load_reviews(path=None):
    if path is None:
        return {}
    entries = json.loads(Path(path).read_text())['reviews']
    result = {}
    for entry in entries:
        if entry.get('status') not in STATUSES or not entry.get('evidence_reference') or not entry.get('reviewer'):
            raise ValueError('Review needs a valid status, evidence reference and reviewer')
        if not re.fullmatch(r'[0-9a-f]{64}', entry.get('page_sha256','')) or not re.fullmatch(r'match_\d+', entry.get('source_id','')):
            raise ValueError('Review must bind a page checksum and source match ID')
        key = (entry['page_sha256'],entry['source_id'])
        if key in result:
            raise ValueError('Duplicate/conflicting status reviews')
        result[key] = entry
    return result


def classify(observation, review):
    """Conservative hints veto acceptance; positive finality needs explicit evidence."""
    text = ' '.join([observation.get('raw_score') or '', observation.get('raw_date') or '', *observation['status_indicators'],
                     *observation['row_classes']]).casefold()
    hints = set()
    for pattern,status in [(r'\b(?:abgebrochen|abandoned)\b','abandoned'),
                           (r'\b(?:abgesagt|cancelled)\b','cancelled'),
                           (r'\b(?:verlegt|postponed)\b','postponed'),
                           (r'\b(?:live|in[- ]progress)\b','live'),
                           (r'\b(?:scheduled|angesetzt)\b','scheduled')]:
        if re.search(pattern,text):hints.add(status)
    administrative = bool(re.search(r'\b(?:awarded|gewertet|annulliert)\b', text))
    state = review['status'] if review else 'unknown'
    issue = None
    if hints:
        if len(hints)>1 or (review and state not in hints):
            return 'unknown', 'status_evidence_conflict', administrative
        state = next(iter(hints))
    if administrative and state != 'awarded':
        issue = 'administrative_outcome_requires_review'
        state = 'unknown'
    if review and state=='awarded':
        if not review.get('outcome_policy'):
            issue = 'awarded_review_needs_outcome_policy'; state='unknown'
        else:
            try:
                confirmed=(exact_integer(review['confirmed_home_goals']),exact_integer(review['confirmed_away_goals']))
                record=observation['record']
                if record is None or confirmed!=(record['home_goals'],record['away_goals']):
                    raise ValueError('awarded score differs from the displayed source result')
            except (KeyError,ValueError) as exc:
                issue='awarded_score_missing_or_conflicting'; state='unknown'
    return state, issue, administrative


def _round_options(html):
    tree = _Tree();tree.feed(html);tree.close()
    select = _one((n for n in tree.root.walk() if n.tag=='select' and n.attrs.get('name')=='matchday_id'), 'round select')
    return {int(n.attrs['value']) for n in select.walk() if n.tag=='option' and str(n.attrs.get('value','')).isdigit()}


def validate_season(fmt, pages, reviews):
    season=fmt['season']; rows=[]; issues=[]; present=set(); invalid_pages=[]
    for entry,content in pages:
        url=entry['url']
        if url not in fmt['urls']:
            continue
        present.add(url)
        try:
            result=parse_dfb_matchday(content.decode('utf-8'), expected_season=season,
                                      expected_matchday=fmt['urls'].index(url)+1)
            if result.source_url != url:
                raise ValueError('Cached canonical URL differs from inventory')
            advertised=_round_options(content.decode('utf-8'))
            if advertised != set(range(1,fmt['rounds']+1)):
                issues.append(dict(code='round_inventory_mismatch',url=url,advertised=sorted(advertised)))
            if result.candidate_rows != fmt['teams']//2:
                issues.append(dict(code='round_fixture_count',url=url,expected=fmt['teams']//2,actual=result.candidate_rows))
            participants=Counter((ob[side+'_key'] or ob[side+'_team'])
                                 for ob in result.observations for side in ('home','away'))
            if len(participants)!=fmt['teams'] or any(n!=1 for n in participants.values()):
                issues.append(dict(code='round_team_participation',url=url,counts=dict(participants)))
            for ob in result.observations:
                review=reviews.get((entry['sha256'],ob['source_id']))
                state,problem,admin=classify(ob,review)
                item=dict(**ob, season=season, matchday=result.matchday, url=url,
                          page_sha256=entry['sha256'], status=state, administrative=admin,
                          status_evidence=review, accepted=False)
                if problem:issues.append(dict(code=problem,source_id=ob['source_id'],url=url))
                # Keys are source slugs when available; names remain untouched in records.
                item['home_identity']=ob['home_key'] or ob['home_team']
                item['away_identity']=ob['away_key'] or ob['away_team']
                if not ob['home_key'] or not ob['away_key']:
                    issues.append(dict(code='team_identity_unverified',source_id=ob['source_id'],url=url))
                if ob['error']:
                    issues.append(dict(code='row_parse_issue',source_id=ob['source_id'],url=url,message=ob['error']))
                if state in ('finished','awarded') and not ob['record']:
                    issues.append(dict(code='finished_without_valid_result',source_id=ob['source_id'],url=url))
                item['accepted']=bool(state in ('finished','awarded') and ob['record'] and not problem)
                rows.append(item)
        except (ValueError,UnicodeError) as exc:
            invalid_pages.append(url); issues.append(dict(code='invalid_page',url=url,message=str(exc)))
    # Never select the last seen version of a fixture: quarantine every collision.
    by_id=defaultdict(list);by_pair=defaultdict(list)
    for row in rows:
        if row['source_id']:by_id[row['source_id']].append(row)
        if row['home_identity'] and row['away_identity']:
            by_pair[(row['home_identity'],row['away_identity'])].append(row)
    for kind,groups in [('source_id',by_id),('fixture',by_pair)]:
        for identity,group in groups.items():
            if len(group)<2:continue
            signatures={json.dumps(r['record'],sort_keys=True) for r in group}
            code='conflicting_records' if len(signatures)>1 else 'duplicate_records'
            issues.append(dict(code=code,kind=kind,identity=identity,
                               references=[dict(url=r['url'],source_id=r['source_id'],sha256=r['page_sha256']) for r in group]))
            for row in group:row['accepted']=False
    labels=defaultdict(set)
    for r in rows:
        for side in ('home','away'):
            identity=r[side+'_identity'];name=r[side+'_team']
            if identity and name:labels[identity].add(name)
    if len(labels)>fmt['teams']:issues.append(dict(code='too_many_team_identities',actual=len(labels)))
    names_to_ids=defaultdict(set)
    for identity,names in labels.items():
        for name in names:names_to_ids[name].add(identity)
    for name,ids in names_to_ids.items():
        if len(ids)>1:issues.append(dict(code='ambiguous_team_label',name=name,identities=sorted(ids)))
    roster_known=(len(labels)==fmt['teams'] and not any(i['code'] in ('team_identity_unverified','ambiguous_team_label') for i in issues))
    possible={(h,a) for h in labels for a in labels if h!=a} if roster_known else set()
    missing_pairs=sorted(possible-set(by_pair))
    accepted=[r['record'] for r in rows if r['accepted']]
    if accepted:
        # Reuse TOTOdology's required-field, calendar, team and goal validator.
        validate_historical_data(pd.DataFrame(accepted))
    accepted_rows=[r for r in rows if r['accepted']]
    home=Counter(r['home_identity'] for r in accepted_rows);away=Counter(r['away_identity'] for r in accepted_rows)
    balance={k:dict(home=home[k],away=away[k]) for k in sorted(labels)}
    uncertain=[r for r in rows if not r['accepted']]
    missing_urls=[dict(matchday=day,url=url) for day,url in enumerate(fmt['urls'],1) if url not in present]
    if fmt['slug'] is None:issues.append(dict(code='season_not_advertised_by_seed'))
    complete=(not fmt['ongoing'] and len(present)==fmt['rounds'] and not invalid_pages
              and len(accepted)==fmt['matches'] and len(labels)==fmt['teams']
              and not uncertain and not missing_pairs and not issues
              and all(v['home']==fmt['teams']-1 and v['away']==fmt['teams']-1 for v in balance.values()))
    return dict(season=season,partition='ongoing' if fmt['ongoing'] else 'completed_history',
                expected_teams=fmt['teams'],expected_matches=fmt['matches'],expected_matchdays=fmt['rounds'],
                acquired_matchdays=len(present),invalid_pages=invalid_pages,
                candidate_rows=len(rows),numeric_results=sum(r['record'] is not None for r in rows),
                accepted_results=len(accepted),observed_teams=len(labels),team_labels={k:sorted(v) for k,v in sorted(labels.items())},
                first_date=min((r['date'] for r in accepted),default=None),last_date=max((r['date'] for r in accepted),default=None),
                candidate_first_date=min((r['record']['date'] for r in rows if r['record']),default=None),
                candidate_last_date=max((r['record']['date'] for r in rows if r['record']),default=None),
                status='COMPLETE' if complete else 'ONGOING_PARTIAL' if fmt['ongoing'] else 'INCOMPLETE',
                issues=issues,missing_matchdays=missing_urls,missing_fixtures=[dict(home_identity=h,away_identity=a) for h,a in missing_pairs],
                missing_fixture_identities_unknown=not roster_known,
                unseen_fixture_slots=max(0,fmt['matches']-len(by_pair)),
                balance=balance,uncertain_matches=uncertain,accepted_matches=accepted_rows,records=accepted)


def build_report(inventory, cache, reviews=None):
    reviews=reviews or {};pages=[]
    for fmt in inventory['seasons']:
        for url in fmt['urls']:
            if url:
                page=cache.get(url)
                if page:pages.append(page)
    seasons=[validate_season(fmt,pages,reviews) for fmt in inventory['seasons']]
    used=set()
    for entry,body in pages:
        try:
            parsed=parse_dfb_matchday(body.decode('utf-8'))
        except (ValueError,UnicodeError):
            continue
        used.update((entry['sha256'],ob['source_id']) for ob in parsed.observations)
    unused=[dict(page_sha256=k[0],source_id=k[1]) for k in reviews if k not in used]
    return dict(source='Official DFB Datencenter only',
                assurance='No numeric score is accepted as final without response-bound status evidence',
                inventory=inventory,provenance=[entry for entry,_ in pages],
                unused_status_reviews=unused,seasons=seasons,
                summary=dict(completed_seasons=sum(s['status']=='COMPLETE' for s in seasons),
                             acquired_matchdays=len(pages),numeric_candidates=sum(s['numeric_results'] for s in seasons),
                             accepted_historical=sum(s['accepted_results'] for s in seasons if s['partition']=='completed_history'),
                             accepted_ongoing=sum(s['accepted_results'] for s in seasons if s['partition']=='ongoing')))


def coverage_markdown(report):
    lines=['# DFB Bundesliga acquisition coverage', '',
           'Numeric results remain uncertain unless final/awarded status has evidence bound to the exact response.',
           'Missing fixture identities are enumerated only when a full team roster can be established; otherwise unknown slots are counted.', '',
           '| Season | Partition | Pages / expected | Numeric candidates | Accepted | Teams / expected | Status |',
           '|---|---|---:|---:|---:|---:|---|']
    for s in report['seasons']:
        lines.append(f"| {s['season']} | {s['partition']} | {s['acquired_matchdays']}/{s['expected_matchdays']} | {s['numeric_results']} | {s['accepted_results']} | {s['observed_teams']}/{s['expected_teams']} | {s['status']} |")
    lines += ['', 'See validation.json for every missing matchday, inferred missing fixture, uncertain match, parse issue and conflict.',
              'Expected match totals for ongoing seasons describe schedule capacity, not finished-result completeness.','']
    return '\n'.join(lines)
