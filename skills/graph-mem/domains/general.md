# Domain: General Purpose

For general knowledge, personal projects, business context, or any domain
without a specific overlay.

## Entity Types

Beyond the core types (`plan`, `implementation`, `decision`, `problem`):

| Type | When to Use |
|------|-------------|
| `person` | An individual — colleague, contact, historical figure |
| `place` | A location — office, city, venue |
| `event` | Something that happened — meeting, launch, incident, milestone |
| `concept` | An idea, topic, or theme |
| `organization` | A company, team, or group |
| `artifact` | A document, product, or created thing |
| `project` | A project or initiative |
| `resource` | A URL, book, tool, or reference material |
| `topic` | A subject area or category for organizing knowledge |

## Relationship Types

| Type | Direction | Example |
|------|-----------|---------|
| `RELATES_TO` | General association | `Concept A` → `Concept B` |
| `PART_OF` | Membership or containment | `Alice` → `Engineering Team` |
| `CAUSED_BY` | Causal link | `Incident` → `Config Change` |
| `LOCATED_IN` | Spatial link | `Office` → `San Francisco` |
| `CREATED_BY` | Authorship | `Document` → `Alice` |
| `OCCURRED_AT` | Event-place link | `Standup` → `Conference Room A` |
| `PARTICIPATED_IN` | Person-event link | `Alice` → `Quarterly Review` |
| `WORKS_AT` | Person-organization link | `Alice` → `Acme Corp` |
| `SUPERSEDES` | Newer replaces older | `Policy v2` → `Policy v1` |

## Extraction Guidance

- Create plans before any significant task, even non-technical ones
- Record outcomes to close the plan → implementation loop
- Prefer specific types — `event` over `concept` for things that happened
- Include temporal info in observations ("meeting occurred on 2026-03-15")
- Link people to organizations and events they participated in
- Store meeting takeaways as observations, not raw transcripts
- Track milestones as dated observations on the project entity
- When learning a topic, create a `topic` entity and link related concepts to it
