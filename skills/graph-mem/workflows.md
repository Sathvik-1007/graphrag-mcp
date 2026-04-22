# Workflows

## Extraction — When New Knowledge Surfaces

After responding to the user, ask: **"Did this turn produce new factual
knowledge?"** If yes, shift into extraction mode. If the turn was purely
mechanical (formatting, acknowledgments, routine tool output), skip extraction.

### When to extract

- A decision was made or a rationale was discussed
- A new concept, person, system, or tool was introduced
- A problem was identified or a root cause discovered
- A plan was formulated or an outcome recorded
- An existing fact was corrected or updated
- Architecture, dependencies, or relationships were discussed

### When to skip extraction

- Purely formatting or stylistic changes
- Acknowledgments ("ok", "sounds good", "thanks")
- Routine tool output with no new insights
- Re-stating what's already in the graph with no new detail
- Temporary exploration that produced nothing worth keeping

### What to look for

Scan the conversation turn — both what the user said and what you responded —
for anything worth persisting:

- **People** mentioned by name or role
- **Systems, services, tools** discussed, used, or referenced
- **Concepts, ideas, methods** introduced or explained
- **Decisions** made, with the reasoning behind them
- **Problems** identified, especially with root causes
- **Plans** formulated, with their goals and constraints
- **Outcomes** of completed work — what happened, what deviated
- **Artifacts** created or modified — files, configs, documents, endpoints

The test: "Would a future session benefit from knowing this exists?" If yes,
it belongs in the graph.

### Before creating anything — search first

For every entity you're about to create, run `search_nodes` with its name. This
is the single most important habit. Duplicates fragment knowledge and make search
unreliable.

- **Exact match**: Add new observations to the existing entity. Update its
  description if it's gone stale.
- **Similar match**: Decide — is this the same thing? If so, add observations.
  If genuinely different, create it with a more specific name.
- **No match**: Create it with `add_entities`.

### After creating — find connections

In a large graph, you can't read everything to know what to connect a new
entity to. Use `suggest_connections` to find semantically related entities:

```
suggest_connections("NewEntity")  → shows similar entities, marks which are already connected
```

Then create relationships for the unconnected ones that genuinely relate.

### Formulate observations

For each entity — new or existing — pull out the atomic facts from this turn.
What was said about it? What changed? What was decided? What was discovered?

One sentence, one fact. Include dates, numbers, specifics. A vague observation
is barely better than no observation.

### Map relationships

Think about how the entities from this turn connect — to each other and to
entities already in the graph. Does A depend on B? Did A cause B? Is A part of
B? Did person A create B?

Create edges with `add_relationships`. Use weight < 1.0 for relationships you're
not fully certain about.

### Self-check before moving on

Before you leave extraction mode, interrogate your work. Ask yourself:

- Did I miss any entities that were mentioned or implied?
- Are my entity types accurate — or could a more specific type fit better?
- Are there implicit relationships I didn't capture? (Co-occurrence in the same
  sentence often signals a relationship.)
- Did I store a conclusion without the reasoning that led to it?
- If a fresh agent started with only this graph, could they reconstruct what
  happened and why?
- Are any existing descriptions now outdated based on what was discussed?

Keep asking until every answer is "yes, I got that." If something feels off,
go back and fix it. This self-check catches what casual extraction misses.

## Starting a Session

Before doing any work, run a health check and recall context:

```
graph_health                        → counts, hotspots, suggested actions
search_nodes("task-relevant query") → find related entities
get_entity("RelevantEntity")        → full context with observations + edges
find_connections("KeyEntity")       → explore the neighborhood
```

### Health check thresholds

After `graph_health`, act on these:

| Condition | Action |
|-----------|--------|
| Entity count > 500 | Review and prune stale/low-value entities |
| Any entity with > 15 observations | Use `compact_observations` to consolidate |
| Missing descriptions > 10% of entities | Add descriptions with `update_entity` |
| Average obs/entity > 10 | Prioritize consolidation across hotspots |

A cold start is a wasted start. Prior decisions, context, and lessons learned
are invisible unless you look for them.

## Ending a Session

Before the session ends:

1. Review what you accomplished — anything not yet stored?
2. Record outcomes of completed work as observations
3. Update descriptions that no longer reflect reality
4. Run `graph_health` to verify the graph is in good shape

## Plans and Implementations

Significant tasks should produce a linked pair:

A **plan** entity (type: `plan`) created before work begins — observations
capture goals, constraints, acceptance criteria. Relates to affected entities
via `TARGETS` or `ADDRESSES`.

An **implementation** entity (type: `implementation`) created after work
completes — observations capture outcomes, deviations, lessons learned. Links
to the plan via `IMPLEMENTS` and to modified entities via `MODIFIES`.

Future sessions search for both to understand *why* something was done (plan)
and *what actually happened* (implementation).

## Handling Duplicates

When you find two entities representing the same thing:

1. `get_entity` on both — compare observations and relationships
2. Confirm they genuinely represent the same real-world concept
3. `merge_entities(target, source)` — source gets absorbed into target
4. `update_entity` on the merged result if the description needs refinement

## Observation Compaction

When an entity accumulates too many observations (15+), consolidate:

1. `get_entity("Name")` — read all observations
2. Group related observations by theme
3. Write merged summaries (preserving dates, numbers, specifics)
4. `compact_observations("Name", keep_ids=[...], new_observations=[...])`

This is atomic — old observations are deleted and new ones added in one step.
No data loss between the delete and the add.

## Periodic Maintenance

Every few sessions, do a health check:

- `graph_health` — review counts, hotspots, missing descriptions
- Look for stale descriptions, orphaned entities, near-duplicate names
- `delete_entities` for things no longer relevant
- `merge_entities` for duplicates that crept in
- `compact_observations` for entities with 15+ observations
- Check open plans — do any need their implementations recorded?

The graph is not an append-only log. It's a living knowledge base. Maintain it.
