# Naming Conventions

Consistent naming makes the knowledge graph searchable and navigable.

## Entity Names

Use **PascalCase** for type-like entities and **descriptive names** for instances:
- `AuthService`, `DatabasePool`, `RateLimiter` (systems/modules)
- `Alice Johnson`, `Dr. Smith` (people — natural names)
- `Decision: Use PostgreSQL`, `Bug: Memory Leak in Worker` (prefixed for clarity)

Avoid: `auth_service`, `the auth service`, `AS`, abbreviations that lose meaning.

## Entity Types

Use **lowercase, singular nouns**:
- `person`, `concept`, `system`, `decision`, `event`, `document`, `tool`

Avoid: `PERSON`, `People`, `person/people`, plural forms.

## Relationship Types

Use **UPPER_SNAKE_CASE verb phrases** describing the direction (source → target):
- `DEPENDS_ON`, `AUTHORED_BY`, `DECIDED_TO`, `RELATES_TO`
- `PART_OF`, `CAUSED_BY`, `IMPLEMENTS`, `USES`

Avoid: `depends-on`, `Depends On`, single nouns like `DEPENDENCY`.

## Observations

Write **complete sentences**, one atomic fact per observation:
- "The API rate limit was increased from 100 to 500 req/s on 2026-03-15"
- "Alice approved the migration plan in the March standup"

Avoid:
- Fragments: "rate limit stuff changed"
- Multiple facts: "Rate limit changed AND we deployed the fix"
- Entire file contents as a single observation
