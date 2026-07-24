# Daily PR auto-merge safety

Daily portfolio pull requests are eligible for squash merge only after three independent gates:

1. the branch and title match the `daily/` automation contract and the diff contains code;
2. every configured PR-associated GitHub check run has completed successfully;
3. the repository test suite passes again from the fetched PR head inside the auto-merge job.

`REQUIRED_CHECK_NAMES` in `.github/workflows/auto-merge-daily-pr.yml` is the explicit check contract. The gate waits for GitHub to register pull-request checks, polls their check-run state for up to 15 minutes, and refuses merge on failure or timeout. Checks attached only to another pull request cannot satisfy the gate.

If a validation job is renamed or added as a merge prerequisite, update `REQUIRED_CHECK_NAMES` in the same pull request. A failed or timed-out gate leaves the PR and linked issue open for diagnosis; it does not bypass validation.

## Backlog validation

Before creating an issue or branch, the daily generator validates the complete backlog as one contract. Task IDs and target paths must be unique, required metadata must be present, and queued Python source must compile. The compile check parses source without importing or executing it, so a malformed task fails locally without running untrusted backlog content or leaving partial GitHub resources behind.
