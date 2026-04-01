# Domain: Software Engineering

## Recommended Entity Types

- `module` — A code module, service, or major component
- `function` — An important function or API endpoint (not every function — just key ones)
- `class` — A significant class or interface
- `api` — An API endpoint or external service integration
- `decision` — An architectural or design decision with rationale
- `bug` — A notable bug with root cause and fix
- `dependency` — An external library or service dependency
- `pattern` — A recurring code pattern or convention

## Recommended Relationship Types

- `IMPORTS` / `DEPENDS_ON` — Module/package dependencies
- `CALLS` — Function/method invocations
- `IMPLEMENTS` — Interface/protocol implementations
- `DECIDED_TO` — Links a decision to what it affects
- `FIXES` — Links a bug to its fix
- `USES` — General usage relationship

## Heuristics

- Store decisions with rationale ("Chose PostgreSQL over MongoDB because we need ACID transactions")
- Track dependency relationships between major modules
- Record bug root causes as observations on the affected entity
- Don't create entities for every file — focus on architectural boundaries
