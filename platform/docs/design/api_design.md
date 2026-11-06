# API application boundary — design notes

## Scope

AetherNet's HTTP integration must expose provider-neutral operations. This
document specifies the route registry and authorization behavior; it does **not**
claim an HTTP server is already running.

## Contracts

- `ApiCommand` represents a **write** route: HTTP method, canonical absolute
  path, stable operation ID and required authorization scope.
- `ApiHandler` registers write routes with unique route keys and operation IDs.
  Identical repeated registration is idempotent; incompatible registration
  fails before changing the registry.
- `ApiQuery` represents a **read** request and constrains pagination.
- `RouteCatalogPort` and `ScopeAuthorizerPort` separate request validation,
  authorization decisions and framework-specific transport.

## Security invariants

1. All state-changing routes require an explicit scope and authorization check.
2. Unknown routes and missing scopes fail closed.
3. A request body must be validated before any mutation, never interpolated
   into an SQL command or shell invocation.
4. Route names and operation identifiers must be stable across releases.
5. Provider credentials stay behind infrastructure adapters; never appear
   in route or query representations.

## Planned HTTP adapter

A future `interfaces/api` implementation translates HTTP requests to typed
commands, authenticates the caller, invokes authorized handlers, and serializes
responses with consistent error semantics. The API adapter and integration
tests are not included in this design-only file.

## Verification

Current command/handler tests check route collisions and denied scopes.
Future HTTP integration tests must demonstrate authentication, forbidden
operations, malformed payloads, and idempotent retries.
