# Domain: Software Engineering

For codebases, software systems, technical architecture, and development workflows.

## Entity Types

Beyond the core types (`plan`, `implementation`, `decision`, `problem`):

| Type | When to Use |
|------|-------------|
| `module` | A code module, service, or major component |
| `function` | A key function or API endpoint — not every function, just important ones |
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
| `CALLS` | Invocation | `LoginHandler` → `AuthService.verify` |
| `IMPLEMENTS` | Interface realization | `JWTAuth` → `AuthInterface` |
| `DECIDED_TO` | Decision affects entity | `Decision: Use JWT` → `AuthService` |
| `FIXES` | Fix resolves bug | `PR #42` → `Bug: Memory Leak` |
| `USES` | General usage | `UserService` → `DatabasePool` |
| `MODIFIES` | Implementation changed entity | `Impl: Refactor Auth` → `AuthService` |
| `INTRODUCES` | Implementation added dependency | `Impl: Add Caching` → `Redis` |
| `TESTED_BY` | Test coverage | `AuthService` → `test_auth.py` |
| `REPLACES` | New replaces old | `AuthServiceV2` → `AuthServiceV1` |

## Extraction Guidance

- Store plans before implementing features — include acceptance criteria
- Record implementation outcomes with deviations from plan
- Store decisions with rationale ("Chose PostgreSQL over MongoDB because ACID")
- Track dependency relationships between major components
- Record bug root causes as observations — high value for future debugging
- Don't create entities for every file — focus on architectural boundaries
- Store configuration decisions as decision entities
- When refactoring, link new implementation to old via `REPLACES`
- Record error messages and stack traces as observations on the bug entity
- Track which tests cover which components with `TESTED_BY`
