# Naming Conventions

Consistent naming makes the knowledge graph searchable and navigable.

## Entity Names

Use **descriptive, natural names** that are easy to find via search:
- `AuthService`, `DatabasePool`, `RateLimiter` (systems/modules — PascalCase)
- `Alice Johnson`, `Dr. Smith` (people — natural names)
- `Attention Is All You Need`, `GPT-4 Technical Report` (papers/documents — title case)
- `Decision: Use PostgreSQL`, `Bug: Memory Leak in Worker` (prefixed for clarity)
- `Plan: Implement Auth Service`, `Implementation: Refactor Search` (workflow entities)
- `Transformer Architecture`, `Reinforcement Learning` (concepts — title case)

Avoid: abbreviations that lose meaning, IDs without context, overly generic names like "Thing 1".

## Entity Types

Use **lowercase, singular nouns**:
- `person`, `concept`, `system`, `decision`, `event`, `document`, `tool`
- `plan`, `implementation`, `problem`
- `paper`, `method`, `finding`, `organization`, `project`

Avoid: `PERSON`, `People`, `person/people`, plural forms.

## Relationship Types

Use **UPPER_SNAKE_CASE verb phrases** describing the direction (source → target):
- `DEPENDS_ON`, `AUTHORED_BY`, `DECIDED_TO`, `RELATES_TO`
- `PART_OF`, `CAUSED_BY`, `IMPLEMENTS`, `USES`
- `CITES`, `CONTRADICTS`, `SUPPORTS`, `EXTENDS`
- `TARGETS`, `MODIFIES`, `INTRODUCES`

Avoid: `depends-on`, `Depends On`, single nouns like `DEPENDENCY`.

## Observations

Write **complete sentences**, one atomic fact per observation:
- "The API rate limit was increased from 100 to 500 req/s on 2026-03-15"
- "Alice approved the migration plan in the March standup"
- "The paper reports a 3.2% improvement on the GLUE benchmark"
- "Decided to use PostgreSQL because we need ACID transactions for billing"

Avoid:
- Fragments: "rate limit stuff changed"
- Multiple facts: "Rate limit changed AND we deployed the fix"
- Raw content dumps as a single observation
