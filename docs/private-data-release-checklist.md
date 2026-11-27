# Preparing a public-safe change set

Private research data and public demonstration content have separate release boundaries.
Keep real source files, derived match datasets, provenance, adjudication notes and
record-bearing test fixtures in ignored local storage. A public demonstration must
use invented fixtures and must not load a private research archive.

The generic offline auditor can check an explicitly supplied CSV:

```sh
python3 -m scripts.audit_match_csv /path/to/local/input.csv --as-of YYYY-MM-DD
```

It checks the eight-column schema, canonical UTF-8/LF serialization, deterministic
IDs, row ordering, duplicate identities, completed-score fields, season boundaries
and future results. Diagnostics contain line numbers and error codes rather than
fixture values. These structural checks do not establish source-use permissions,
settle historical ambiguities or prove season completeness. Keep audit results
private when they concern real inputs.

Before proposing a public commit:

1. Review an explicit file allowlist containing only generic code, tests with
   invented inputs, schemas and non-sensitive documentation.
2. Inspect the actual diff and index. An ignore rule does not remove a file that
   is already tracked. Review existing tracked data and repository history before
   any publication; a safe new patch does not make earlier history safe.
3. Exclude private CSVs, source snapshots, record-bearing reports, screenshots,
   logs and generated test output. Review planning logs separately: they may
   contain private research details even when stored outside the private folder.
4. Verify that tests do not require private archives and that no default path,
   network request or upload can expose local data.
5. Run focused tests and the applicable regression suite. Inspect serialization
   and provenance independently for private dataset releases.
6. Obtain the owner's separate approval for staging, committing, pushing or
   integrating branches. Preserve unrelated work and existing datasets throughout.

This checklist prepares a reviewable patch; it performs no Git mutation or publication.
