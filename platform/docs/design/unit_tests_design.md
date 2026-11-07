# Platform & QA: Unit Tests design

**Registry artifact:** AET-0025  
**Status:** Deterministic reference scaffold; provider integration remains future work.

## Responsibility

The **unit_tests** feature belongs to the **Platform & QA** subsystem. Its planned layer is **docs/design**. It must offer provider-neutral identifiers, immutable read requests, deliberate write authorization, and traceable error handling.

## Data and behavior

- Reject blank resource identifiers and unsupported mutation types.
- Preserve explicit revision and resource identity through every boundary.
- Keep domain decisions deterministic and independent of cloud SDKs.
- Distinguish read-side queries from commands that can change state.
- Treat absent credentials, incomplete evidence and inconsistent state as errors.

## Interface contract

A UnitTests command requests a validated operation; a handler orchestrates that operation through an injected port. Adapters must map external responses to typed records. Persistence is behind a repository contract; HTTP serialization must not own domain decisions.

## Operational concerns

Retries should be idempotent, failures should be observable, and secrets must stay outside committed source. Audit the resource, operation, revision and outcome without exposing credentials or sensitive payloads.

## Verification plan

Implement real provider fixtures and explicit authorization/negative tests when a production integration is added. This document makes no claim that the integration or those tests already exist.
