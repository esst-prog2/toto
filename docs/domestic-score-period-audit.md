# Domestic score-period audit — accepted findings

Accepted by the owner on 2026-11-26. This public summary contains aggregate findings;
the detailed report and event-level evidence remain private and Git-ignored.

The read-only audit counted 156,579 unique standardized records in 16 CSVs across
14 domestic competitions, including the two ongoing English snapshots. No identified
extra-time or shootout contamination requires a standardized dataset correction.
The separate 1,312-row application dataset reconciled to its regular-season originals.
Synthetic demonstration data was distinguished from actual historical evidence.

Acquired Serie B sources contain 15 explicitly marked extra-time events, three with
shootouts. Thirteen leading score pairs differ from the regulation-time score.
All are among 120 excluded postseason observations; no excluded source locator appears
in the standardized source links. Four excluded intermediate records omit the period
annotation retained by their original text; two expose a leading shootout tally in
generic goal fields. Those representations must not be reused as regulation scores.

Belgium's two included European qualification finals have supporting regulation-time
results. Its other included postseason groups and the 1991/92 2. Bundesliga second-phase
groups are league structures, not presumed extra-time knockouts. Existing domestic
scope exclusions and administrative-result decisions remain unchanged.

Evidence combined source conventions, raw annotations, season/stage accounting,
source-to-output exclusion links and targeted match/rule documentation. It is not
universal external certification of every fixture or every historical rulebook.
Missing periods and acquisition gaps must remain explicit.

The complete accepted temporary audit was copied byte-for-byte, without deleting its
original, to `data/private/audits/domestic_score_period/2026-11-26/`. Its preservation
manifest identifies every copied report, evidence registry, script and checksum.
Nothing in that archive is authorized for publication or model training.

The audit took 18 minutes 14 seconds and verified 2,332 unchanged preservation
fingerprints. It changed no dataset, code, schema, planning log, Git state or environment.
The subsequent owner-authorized documentation and Champions League Phase 2 work are
separate from that frozen audit. See [PROCESS.md](../PROCESS.md) for the accepted
project-wide regulation-time requirement and preserved administrative policy.
