# Domain: General Purpose

## Recommended Entity Types

In addition to the core types (`plan`, `implementation`, `decision`):

- `person` — An individual (colleague, contact, historical figure)
- `place` — A location (office, city, venue)
- `event` — Something that happened (meeting, launch, incident)
- `concept` — An idea, topic, or theme
- `organization` — A company, team, or group
- `artifact` — A document, product, or created thing
- `project` — A project or initiative

## Recommended Relationship Types

- `RELATES_TO` — General association
- `PART_OF` — Membership or containment
- `CAUSED_BY` — Causal relationships
- `LOCATED_IN` — Spatial relationships
- `CREATED_BY` — Authorship or creation
- `OCCURRED_AT` — Event-place relationships
- `TARGETS` — Links a plan to the entities it will affect
- `IMPLEMENTS` — Links an implementation to the plan it fulfils

## Heuristics

- Store plans before starting any significant task, even non-technical ones
- Record implementation outcomes to close the plan→implementation loop
- Use the most specific entity type that fits — prefer "event" over "concept" for things that happened
- Record temporal information in observations ("The meeting occurred on 2026-03-15")
- Link people to organizations and events they participated in
- For personal knowledge management, focus on connections between ideas
