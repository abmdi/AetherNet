# CI evidence and release gates — design notes

## Scope

AetherNet treats CI observations as immutable evidence for an exact source
revision. Job status from a different revision cannot authorize publication.
The current modules describe application contracts; they are not a completed
CI vendor integration.

## Contracts

- `CiCommand` pins an explicit revision and a unique nonempty set of required
  check names. A missing or pending check never passes.
- `CiHandler` evaluates named `CheckResult` records and rejects stale,
  missing, failed or pending checks.
- `CiQuery` selects read-only observations with bounded pagination and
  optional name filters.
- `CiStatusPort` retrieves revision-bound `JobObservation` records, while
  `RevisionResolverPort` resolves mutable refs to immutable commits.

## Required behavior

1. Resolve a branch or tag to an immutable commit SHA before requesting checks.
2. Tie every observed check to that immutable SHA; never rely on branch names
   alone or on untrusted check names supplied by a release candidate.
3. Treat cancelled, failed, missing, stale and pending checks as nonpassing.
4. Validate file hashes and repository cleanliness before publishing.
5. Report the exact revision, required checks and outcome for auditability.

## Threats and failure modes

- **Stale success:** a check for an earlier commit is incorrectly reused.
- **Partial success:** a runner completed some checks but mandatory checks
  are missing.
- **Race:** the branch tip changes between CI evaluation and publication.
- **Outage:** no current check observations are available.

In each case publication must fail closed. Scheduling a job is not proof that
the job ran, and a successful workflow is not proof of minute-accurate commits.

## Planned adapters

A future infrastructure adapter will retrieve CI status from a configured
provider. It must authenticate without embedding credentials in public
artifacts, implement bounded retries, and provide integration tests using
recorded fixtures. No provider adapter is implemented in this design file.
