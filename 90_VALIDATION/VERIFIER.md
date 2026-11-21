# PPKT VERIFY | release-integrity framework

1. `scripts/check_core.py`: machine checks for required authority files, valid JSON, registered paths, rejected prohibited claims/commingling and brand/product statuses. CI can pass when those consistency tests pass.
2. `scripts/release_readiness.py`: evidence-sensitive prelaunch check. Defaults to **blocked** when any gate UNKNOWN, missing ratification, missing reviewer, absent evidence or comparator measurements. `--enforce` deliberately fails a controlled release job.
3. `tests/`: exercises successful structural checks, deliberate invalidation, stale/false approvals and blocking absent measurements.
4. Security/reconciliation and external attestations cannot be inferred from this static repository. Later build milestones must add real unit/integration/invariant tests, audited deployments and independent reviews.

**Integrity rule:** No script may write `adopted`, `licensed`, `attested` or `ready` as a side effect of CI. An evidence path must point to real recorded evidence. Do not include identity, banking or sensitive files in public Git.
