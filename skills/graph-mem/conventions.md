# Naming Conventions

Consistent naming makes the knowledge graph searchable, navigable, and mergeable
across sessions. These conventions are mandatory, not suggestions.

## Entity Names

**Rule: Descriptive, natural, searchable. A future search must find this entity.**

| Category | Pattern | Examples |
|----------|---------|----------|
| Systems/modules | PascalCase | `AuthService`, `DatabasePool`, `RateLimiter` |
| People | Natural names | `Alice Johnson`, `Dr. Smith` |
| Papers/documents | Title case | `Attention Is All You Need` |
| Prefixed workflow | `Prefix: Description` | `Decision: Use PostgreSQL`, `Bug: Memory Leak` |
| Concepts | Title case | `Transformer Architecture`, `Dependency Injection` |

**Never**: abbreviations that lose meaning (`AS` instead of `AuthService`), bare IDs
(`#1234`), or generic names (`Thing 1`, `Misc`).

## Entity Types

**Rule: Lowercase, singular nouns. Always.**

Core types: `person`, `concept`, `system`, `decision`, `event`, `document`, `tool`,
`plan`, `implementation`, `problem`, `project`

**Never**: `PERSON`, `People`, `person/people`, plural forms, PascalCase types.

## Relationship Types

**Rule: UPPER_SNAKE_CASE verb phrases describing the direction (source → target).**

| Category | Types |
|----------|-------|
| Dependencies | `DEPENDS_ON`, `USES`, `REQUIRES` |
| Authorship | `AUTHORED_BY`, `CREATED_BY`, `OWNED_BY` |
| Structure | `PART_OF`, `CONTAINS`, `EXTENDS` |
| Causation | `CAUSED_BY`, `FIXES`, `ADDRESSES` |
| Workflow | `IMPLEMENTS`, `TARGETS`, `MODIFIES`, `INTRODUCES` |
| Knowledge | `CITES`, `CONTRADICTS`, `SUPPORTS`, `RELATES_TO` |
| Temporal | `FOLLOWS_FROM`, `SUPERSEDES`, `PRECEDED_BY` |

**Never**: `depends-on`, `Depends On`, bare nouns like `DEPENDENCY`.

## Observations

**Rule: Complete sentences. One atomic fact per observation. Include specifics.**

Good:
- "The API rate limit was increased from 100 to 500 req/s on 2026-03-15"
- "Alice approved the migration plan during the March standup"
- "Decided to use PostgreSQL because we need ACID transactions for billing"

Bad:
- "rate limit stuff changed" (fragment, no specifics)
- "Rate limit changed AND we deployed the fix" (two facts in one)
- *Entire paragraph pasted as one observation* (not atomic)

## Descriptions

**Rule: Every entity MUST have a non-empty description. The description summarizes
what this entity IS, not what happened to it.**

Good: "A JWT-based authentication service that handles user login, token refresh,
and session management"

Bad: "" (empty), "auth stuff", "The thing we discussed"
