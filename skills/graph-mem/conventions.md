# Naming Conventions

Consistent naming makes the graph searchable and mergeable across sessions.

## Entity Names

Names must be descriptive, natural, and findable by search.

| Category | Pattern | Examples |
|----------|---------|----------|
| Systems / modules | PascalCase | `AuthService`, `DatabasePool` |
| People | Natural names | `Alice Johnson`, `Dr. Smith` |
| Documents / papers | Title case | `Attention Is All You Need` |
| Prefixed workflow items | `Prefix: Description` | `Decision: Use PostgreSQL`, `Bug: Memory Leak` |
| Concepts / ideas | Title case | `Dependency Injection`, `Event Sourcing` |

Avoid abbreviations that lose meaning (`AS` instead of `AuthService`), bare IDs
(`#1234`), or generic names (`Thing 1`, `Misc`). A future search must find this
entity by what it actually is.

## Entity Types

Lowercase, singular nouns. Always.

Use the most specific type that fits. Common types: `person`, `concept`, `system`,
`decision`, `event`, `document`, `tool`, `plan`, `implementation`, `problem`,
`project`. Domain overlays add more.

Never: `PERSON`, `People`, plurals, PascalCase types.

## Relationship Types

UPPER_SNAKE_CASE verb phrases that read naturally in the direction source → target.

| Category | Examples |
|----------|---------|
| Dependencies | `DEPENDS_ON`, `USES`, `REQUIRES` |
| Authorship | `AUTHORED_BY`, `CREATED_BY`, `OWNED_BY` |
| Structure | `PART_OF`, `CONTAINS`, `EXTENDS` |
| Causation | `CAUSED_BY`, `FIXES`, `ADDRESSES` |
| Workflow | `IMPLEMENTS`, `TARGETS`, `MODIFIES`, `INTRODUCES` |
| Knowledge | `CITES`, `CONTRADICTS`, `SUPPORTS`, `RELATES_TO` |
| Temporal | `FOLLOWS_FROM`, `SUPERSEDES`, `PRECEDED_BY` |

Never: `depends-on`, `Depends On`, bare nouns like `DEPENDENCY`.

## Observations

Complete sentences. One atomic fact per observation. Include specifics — dates,
numbers, file paths, exact values.

Good:
- "The API rate limit was increased from 100 to 500 req/s on 2026-03-15"
- "Decided to use PostgreSQL because we need ACID transactions for billing"

Bad:
- "rate limit stuff changed" (vague, no specifics)
- "Rate limit changed AND we deployed the fix" (two facts crammed into one)
- An entire paragraph pasted as one observation (not atomic)

## Descriptions

Every entity must have a non-empty description that says what this entity IS —
not what happened to it.

Good: "A JWT-based authentication service handling login, token refresh, and
session management"

Bad: "" (empty), "auth stuff", "The thing we discussed"
