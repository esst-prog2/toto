"""Offline parser for DFB's observed c-MatchTable HTML, never a downloader.

Only the Bundesliga league_matches result frame is parsed. Unknown layouts fail
closed; unscored or ambiguous rows are reported, not converted to zero goals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
import re
from urllib.parse import urlsplit

from .historical_import import canonical_season
from .validation import exact_integer, team_name

COLUMNS = ('season', 'matchday', 'date', 'home_team', 'away_team', 'home_goals', 'away_goals')


@dataclass
class Node:
    tag: str
    attrs: dict[str, str | None] = field(default_factory=dict)
    children: list = field(default_factory=list)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def has_class(self, name):
        return name in (self.attrs.get('class') or '').split()

    def text(self):
        if self.tag in ('script', 'style'):
            return ''
        return ' '.join(c.text() if isinstance(c, Node) else c for c in self.children)


class _Tree(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def _one(nodes, label):
    items = list(nodes)
    if len(items) != 1:
        raise ValueError(f'expected exactly one {label}, found {len(items)}')
    return items[0]


def _text(node):
    return ' '.join(node.text().split())


@dataclass
class DfbParseResult:
    records: list[dict]
    issues: list[dict]
    source_url: str
    season: str
    matchday: int
    candidate_rows: int
    observations: list[dict] = field(default_factory=list)


def parse_dfb_matchday(html: str, *, expected_season=None, expected_matchday=None,
                       expected_matches=None) -> DfbParseResult:
    """Parse a saved full HTML page; expected counts are caller-supplied, not nine.

    Numeric scores on this historical page are result candidates, not independent
    proof of finished status. Future/live pages need a verified status policy.
    """
    tree = _Tree()
    tree.feed(html)
    tree.close()
    root = tree.root
    canonical = _one((n for n in root.walk() if n.tag=='link' and n.attrs.get('rel')=='canonical'), 'canonical link')
    url = canonical.attrs.get('href') or ''
    parsed_url = urlsplit(url)
    path = re.fullmatch(r'/de/competitions/bundesliga/seasons/([0-9]{4}-[0-9]{2,4})/matchday/([0-9]+)', parsed_url.path)
    if parsed_url.hostname != 'datencenter.dfb.de' or not path:
        raise ValueError('canonical URL is not a supported Bundesliga matchday page')
    season = canonical_season(path[1])
    day = exact_integer(path[2])
    if '/' not in season or day < 1:
        raise ValueError('invalid season or matchday')
    if expected_season is not None and canonical_season(expected_season) != season:
        raise ValueError('unexpected season')
    if expected_matchday is not None and exact_integer(expected_matchday) != day:
        raise ValueError('unexpected matchday')
    for name, value in (('season_id', season), ('matchday_id', day)):
        select = _one((n for n in root.walk() if n.tag=='select' and n.attrs.get('name')==name), name+' select')
        option = _one((n for n in select.walk() if n.tag=='option' and 'selected' in n.attrs), name+' selected option')
        actual = canonical_season(option.attrs.get('value') or '') if name=='season_id' else exact_integer(option.attrs.get('value') or '')
        if actual != value:
            raise ValueError('canonical URL and selected filters disagree')
    frame = _one((n for n in root.walk() if n.attrs.get('id')=='league_matches'), 'league_matches frame')
    body = _one((n for n in frame.walk() if n.has_class('c-MatchTable-body')), 'match result body')
    rows = [n for n in body.children if isinstance(n, Node) and n.has_class('c-MatchTable-row')]
    if not rows:
        raise ValueError('no match rows in result body (layout change or empty page)')
    records, issues, ids, fixtures = [], [], set(), set()
    observations = []
    for index, row in enumerate(rows, 1):
        # Retain identity/status evidence even when dates or scores cannot be parsed.
        observation = dict(row=index, source_id=None, home_team=None, away_team=None,
                           home_key=None, away_key=None, raw_date=None, raw_score=None,
                           status_indicators=[], record=None, error=None)
        if re.search(r'\b(?:gewertet|awarded|annulliert|Sportgericht)\b', _text(row), re.IGNORECASE):
            observation['status_indicators'].append('administrative: awarded/gewertet')
        for node in row.walk():
            marker_id = node.attrs.get('id') or ''
            if re.fullmatch(r'match_[0-9]+', marker_id):
                observation['source_id'] = marker_id
                observation['raw_date'] = _text(node)
            if node.has_class('c-MatchTable-score'):
                observation['raw_score'] = _text(node)
            if node.has_class('c-MatchTable-status'):
                observation['status_indicators'].append(_text(node))
            if node.attrs.get('data-match-status'):
                observation['status_indicators'].append(node.attrs['data-match-status'])
            for side in ('home', 'away'):
                if node.has_class(f'c-MatchTable-team--{side}'):
                    links = [n for n in node.walk() if n.tag == 'a']
                    if len(links) == 1:
                        observation[side+'_team'] = _text(links[0])
                        team_path = urlsplit(links[0].attrs.get('href') or '').path
                        key = re.search(r'/teams/([^/]+)$', team_path)
                        observation[side+'_key'] = key[1] if key else None
        observation['row_classes'] = (row.attrs.get('class') or '').split()
        observations.append(observation)
        try:
            marker = _one((n for n in row.walk() if re.fullmatch(r'match_[0-9]+', n.attrs.get('id') or '')), 'source match ID')
            home_node = _one((n for n in row.walk() if n.has_class('c-MatchTable-team--home')), 'home team')
            away_node = _one((n for n in row.walk() if n.has_class('c-MatchTable-team--away')), 'away team')
            home = team_name(_text(_one((n for n in home_node.walk() if n.tag=='a'), 'home name link')))
            away = team_name(_text(_one((n for n in away_node.walk() if n.tag=='a'), 'away name link')))
            if not home or not away or home == away:
                raise ValueError('missing or identical teams')
            dates = re.findall(r'(?<![0-9])([0-9]{2})\.([0-9]{2})\.([0-9]{4})(?![0-9])', _text(marker))
            d, m, y = map(int, _one(dates, 'German match date'))
            match_date = date(y,m,d)
            if y not in map(int, season.split('/')):
                raise ValueError('date outside season calendar years')
            score_node = _one((n for n in row.walk() if n.has_class('c-MatchTable-score')), 'score container')
            score_link = _one((n for n in score_node.walk() if n.tag=='a'), 'score link')
            score_path = urlsplit(score_link.attrs.get('href') or '').path
            link_scope = re.match(r'/datencenter/bundesliga/([0-9]{4}-[0-9]{2,4})/([0-9]+)-spieltag/', score_path)
            if not link_scope or canonical_season(link_scope[1]) != season or int(link_scope[2]) != day:
                raise ValueError('score link belongs to another competition/season/matchday')
            score = re.fullmatch(r'([0-9]+)\s*:\s*([0-9]+)(?:\s*\[(?:awarded|gewertet)\])?', _text(score_node), re.IGNORECASE)
            if not score:
                raise ValueError('unscored/ambiguous score or unsupported match status; not a finished result')
            h, a = map(exact_integer, score.groups())
            identity = (match_date.isoformat(),home,away)
            if marker.attrs['id'] in ids or identity in fixtures:
                raise ValueError('duplicate source ID or fixture')
            ids.add(marker.attrs['id'])
            fixtures.add(identity)
            record = dict(zip(COLUMNS,(season,day,match_date.isoformat(),home,away,h,a)))
            observation['record'] = record
            records.append(record)
        except ValueError as exc:
            observation['error'] = str(exc)
            issues.append(dict(row=index, code='invalid_match_row', message=str(exc)))
    if expected_matches is not None and (len(rows)!=expected_matches or len(records)!=expected_matches):
        raise ValueError(f'expected {expected_matches} matches; candidate rows={len(rows)}, parsed={len(records)}, issues={issues}')
    return DfbParseResult(records,issues,url,season,day,len(rows),observations)
