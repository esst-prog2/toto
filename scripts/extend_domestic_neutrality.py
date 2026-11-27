"""Hash-guarded v1-to-v2 metadata migration; no acquisition or historical repairs.

Prepare privately first, inspect the preservation report, then explicitly apply.
Frozen originals, audit archives and unstandardized inputs are never targets.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
from scripts.artifact_io import check_overwrite, serialize_csv
from toto_estimator.match_schema import LEGACY_COLUMNS, CANONICAL_COLUMNS, neutral_value, validate_canonical_records

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / 'data/private/europe/champions_league/phase4'


def digest(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(path.read_bytes())
def require(test, message):
    if not test: raise ValueError(message)


def extend_bytes(raw, classification):
    value = neutral_value(classification)
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8'), newline=''), strict=True)
    require(tuple(reader.fieldnames or ()) == LEGACY_COLUMNS, 'Migration requires exact v1 columns')
    records = list(reader)
    require(all(None not in r and all(v is not None for v in r.values()) for r in records), 'Malformed original CSV')
    extended = [dict(r, neutral_venue=value) for r in records]
    validate_canonical_records(extended, require_order=False)
    payload = serialize_csv(extended, CANONICAL_COLUMNS)
    # This byte-level projection also checks quoting, Unicode and row ordering.
    projection = serialize_csv(({k: r[k] for k in LEGACY_COLUMNS} for r in extended), LEGACY_COLUMNS)
    require(projection == raw, 'Legacy byte projection differs; refuse normalization')
    return payload, {'original_rows': len(records), 'extended_rows': len(extended), 'original_columns': 8, 'extended_columns': 9,
                     'unchanged_preexisting_fields': len(records) * 8, 'changed_preexisting_fields': 0, 'changed_match_ids': 0,
                     'neutral_0': len(records) if value == 0 else 0, 'neutral_1': len(records) if value == 1 else 0,
                     'neutral_NA': len(records) if value is None else 0, 'legacy_projection_byte_identical': True}


def prepare(plan_path, output):
    output = Path(output).resolve()
    require(not output.is_relative_to(ROOT) or output.is_relative_to(ROOT / 'data/private'), 'Preparation must remain private')
    plan = read(plan_path); targets = plan['targets']; outputs = []
    for target in targets:
        path = ROOT / target['path']; backup = ROOT / target['backup']
        require(path.resolve().is_relative_to(ROOT / 'data/private') and 'standardized' in path.name and 'audit' not in path.name, 'Non-standardized target forbidden')
        require(backup.resolve().is_relative_to(PHASE / 'backups'), 'Backup outside immutable migration workspace')
        raw = backup.read_bytes()
        require(digest(raw) == target['sha256'] and path.read_bytes() == raw, 'Target or frozen backup changed')
        payload, report = extend_bytes(raw, target['neutral_venue'])
        require(report['original_rows'] == target['rows'], 'Approved row count changed')
        dest = output / target['path']
        outputs.append((dest, payload, dict(report, path=target['path'], before_sha256=digest(raw), after_sha256=digest(payload), basis=target['basis'])))
    require(len({str(p) for p, _, _ in outputs}) == len(targets), 'Duplicate migration target')
    check_overwrite([p for p, _, _ in outputs] + [output / 'preservation_report.json'])
    for dest, payload, _ in outputs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as handle: handle.write(payload)
    report = {'schema_version': 2, 'plan_sha256': digest(Path(plan_path).read_bytes()), 'files': [r for _, _, r in outputs],
              'total_rows': sum(t['rows'] for t in targets), 'file_count': len(targets), 'status': 'PREPARED_NOT_APPLIED'}
    (output / 'preservation_report.json').write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    return report


def apply(plan_path, prepared, receipt):
    prepared = Path(prepared).resolve(); receipt = Path(receipt).resolve()
    for location in (prepared, receipt):
        require(not location.is_relative_to(ROOT) or location.is_relative_to(ROOT / 'data/private'), 'Migration metadata must remain private')
    plan = read(plan_path); report = read(prepared / 'preservation_report.json')
    require(report['plan_sha256'] == digest(Path(plan_path).read_bytes()), 'Migration plan changed')
    check_overwrite([Path(receipt)])
    changes = []
    for target, comparison in zip(plan['targets'], report['files'], strict=True):
        path = ROOT / target['path']; payload = (prepared / target['path']).read_bytes()
        require(path.resolve().is_relative_to(ROOT / 'data/private') and 'standardized' in path.name and 'audit' not in path.name, 'Non-standardized target forbidden')
        require((ROOT / target['backup']).resolve().is_relative_to(PHASE / 'backups'), 'Backup outside immutable migration workspace')
        require(path.read_bytes() == (ROOT / target['backup']).read_bytes() and digest(path.read_bytes()) == target['sha256'], 'Pre-application target changed')
        require(comparison['path'] == target['path'] and digest(payload) == comparison['after_sha256'], 'Prepared output changed')
        independently_prepared, _ = extend_bytes((ROOT / target['backup']).read_bytes(), target['neutral_venue'])
        require(payload == independently_prepared, 'Prepared output does not match approved extension')
        changes.append((path, payload))
    # All preconditions are checked before the first approved target is replaced.
    for path, payload in changes:
        temp = path.with_name(path.name + '.neutral-v2.tmp')
        try:
            with temp.open('xb') as handle: handle.write(payload)
            os.replace(temp, path)
        finally:
            if temp.exists(): temp.unlink()
    result = dict(report, status='APPLIED_APPROVED_METADATA_ONLY')
    with Path(receipt).open('x') as handle: json.dump(result, handle, sort_keys=True, indent=2); handle.write('\n')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--plan', type=Path, default=PHASE / 'domestic_migration_plan.json')
    p.add_argument('--output', type=Path, default=PHASE / 'domestic_prepared'); p.add_argument('--apply', action='store_true'); p.add_argument('--receipt', type=Path, default=PHASE / 'domestic_migration_applied.json')
    a = p.parse_args(); result = apply(a.plan, a.output, a.receipt) if a.apply else prepare(a.plan, a.output)
    print(json.dumps({k: v for k, v in result.items() if k != 'files'}, indent=2))
