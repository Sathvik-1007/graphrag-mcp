# Domain: Software Engineering

When working on codebases, software systems, or technical architecture.

## Entity Types

In addition to the core types (`plan`, `implementation`, `decision`, `problem`):

| Type | When to Use |
|------|-------------|
| `module` | A code module, service, or major component |
| `function` | A key function or API endpoint (not every function — just important ones) |
| `class` | A significant class or interface |
| `api` | An API endpoint or external service integration |
| `bug` | A notable bug with root cause and fix |
| `dependency` | An external library or service dependency |
| `pattern` | A recurring code pattern or convention |
| `architecture` | A high-level system design or architectural decision |
| `config` | A configuration setting, environment variable, or deployment parameter |

## Relationship Types

| Type | Direction | Example |
|------|-----------|---------|
| `IMPORTS` / `DEPENDS_ON` | Module dependencies | `AuthService` → `JWT Library` |
| `CALLS` | Function invocations | `LoginHandler` → `AuthService.verify` |
| `IMPLEMENTS` | Interface implementations | `JWTAuth` → `AuthInterface` |
| `DECIDED_TO` | Decision affects entity | `Decision: Use JWT` → `AuthService` |
| `FIXES` | Fix resolves bug | `PR #42` → `Bug: Memory Leak` |
| `USES` | General usage | `UserService` → `DatabasePool` |
| `MODIFIES` | Implementation changed entity | `Impl: Refactor Auth` → `AuthService` |
| `INTRODUCES` | Implementation added dependency | `Impl: Add Caching` → `Redis` |
| `TESTED_BY` | Component test coverage | `AuthService` → `test_auth.py` |
| `REPLACES` | New code replaces old | `AuthServiceV2` → `AuthServiceV1` |

## Extraction Heuristics

- Store plans before implementing features — include acceptance criteria as observations
- Record implementation outcomes with deviations from the plan
- Store decisions with rationale ("Chose PostgreSQL over MongoDB because we need ACID")
- Track dependency relationships between major modules
- Record bug root causes as observations — these are high-value for future debugging
- Don't create entities for every file — focus on architectural boundaries and key components
- Store configuration decisions as decision entities
- When refactoring, link the new implementation to the old via `REPLACES`
- Record error messages and stack traces as observations on the relevant bug entity
- Track which tests cover which components with `TESTED_BY` relationships
