# Domain: General Purpose

When managing general knowledge, personal projects, business context, or any domain
not covered by a specific overlay.

## Entity Types

In addition to the core types (`plan`, `implementation`, `decision`, `problem`):

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
| `CAUSED_BY` | Causal relationships | `Incident` → `Config Change` |
| `LOCATED_IN` | Spatial relationships | `Office` → `San Francisco` |
| `CREATED_BY` | Authorship or creation | `Document` → `Alice` |
| `OCCURRED_AT` | Event-place link | `Standup Meeting` → `Conference Room A` |
| `PARTICIPATED_IN` | Person-event link | `Alice` → `Quarterly Review` |
| `WORKS_AT` | Person-organization link | `Alice` → `Acme Corp` |
| `SUPERSEDES` | Newer replaces older | `Policy v2` → `Policy v1` |

## Extraction Heuristics

- Store plans before starting any significant task, even non-technical ones
- Record implementation outcomes to close the plan → implementation loop
- Use the most specific entity type — prefer `event` over `concept` for things that happened
- Include temporal information in observations ("The meeting occurred on 2026-03-15")
- Link people to organizations and events they participated in
- Store meeting notes as observations on the meeting entity, not as raw transcripts
- Track project milestones as observations on the project entity with dates
- When learning a new topic, create a `topic` entity and link related concepts to it
