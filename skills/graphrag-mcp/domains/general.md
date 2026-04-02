# Domain: General Purpose

When managing general knowledge, personal projects, business context, or any domain
not covered by a specific overlay.

## Recommended Entity Types

In addition to the core types (`plan`, `implementation`, `decision`):

- `person` — An individual (colleague, contact, historical figure)
- `place` — A location (office, city, venue)
- `event` — Something that happened (meeting, launch, incident, milestone)
- `concept` — An idea, topic, or theme
- `organization` — A company, team, or group
- `artifact` — A document, product, or created thing
- `project` — A project or initiative
- `resource` — A URL, book, tool, or reference material
- `topic` — A subject area or category for organizing knowledge

## Recommended Relationship Types

- `RELATES_TO` — General association
- `PART_OF` — Membership or containment
- `CAUSED_BY` — Causal relationships
- `LOCATED_IN` — Spatial relationships
- `CREATED_BY` — Authorship or creation
- `OCCURRED_AT` — Event-place relationships
- `PARTICIPATED_IN` — Person-event relationships
- `WORKS_AT` — Person-organization relationships
- `TARGETS` — Links a plan to the entities it will affect
- `IMPLEMENTS` — Links an implementation to the plan it fulfils
- `SUPERSEDES` — Newer version replacing older

## Heuristics

- Store plans before starting any significant task, even non-technical ones
- Record implementation outcomes to close the plan→implementation loop
- Use the most specific entity type that fits — prefer "event" over "concept" for things that happened
- Record temporal information in observations ("The meeting occurred on 2026-03-15")
- Link people to organizations and events they participated in
- For personal knowledge management, focus on connections between ideas — that's where the graph's value lies
- Store meeting notes as observations on the meeting event entity, not as raw transcripts
- Track project milestones as observations on the project entity with dates
- When learning a new topic, create a `topic` entity and link related concepts to it
