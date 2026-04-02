# Domain: Software Engineering

## Recommended Entity Types

In addition to the core types (`plan`, `implementation`, `decision`):

- `module` — A code module, service, or major component
- `function` — An important function or API endpoint (not every function — just key ones)
- `class` — A significant class or interface
- `api` — An API endpoint or external service integration
- `bug` — A notable bug with root cause and fix
- `dependency` — An external library or service dependency
- `pattern` — A recurring code pattern or convention

## Recommended Relationship Types

- `IMPORTS` / `DEPENDS_ON` — Module/package dependencies
- `CALLS` — Function/method invocations
- `IMPLEMENTS` — Interface/protocol implementations (also: plan→implementation links)
- `DECIDED_TO` — Links a decision to what it affects
- `FIXES` — Links a bug to its fix
- `USES` — General usage relationship
- `TARGETS` — Links a plan to the entities it will modify
- `MODIFIES` — Links an implementation to the entities it changed
- `INTRODUCES` — Links an implementation to new dependencies added

## Heuristics

- Store plans before implementing features — include acceptance criteria as observations
- Record implementation outcomes with deviations from the plan
- Store decisions with rationale ("Chose PostgreSQL over MongoDB because we need ACID transactions")
- Track dependency relationships between major modules
- Record bug root causes as observations on the affected entity
- Don't create entities for every file — focus on architectural boundaries
