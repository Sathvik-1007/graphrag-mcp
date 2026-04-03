# Workflows

## The Double-Pass Pipeline (Every Turn)

This pipeline runs on EVERY conversation turn. No exceptions.

### Pass 1: Respond

Do your normal work. Answer the question, write the code, debug the issue. Focus
100% on the user's request. Do not split attention to the graph during this pass.

### Pass 2: Extract and Store

After your response is complete, enter extraction mode. This is a systematic process,
not a vague "store what feels important."

#### Step 1: Entity Extraction

Scan the conversation turn (both user message and your response) for:

- **People** mentioned by name or role
- **Systems, services, or tools** discussed or used
- **Concepts or ideas** introduced or referenced
- **Decisions** made (with rationale)
- **Problems** identified (with root cause if known)
- **Plans** formulated (with steps)
- **Implementations** completed (with outcomes)
- **Artifacts** created or modified (files, configs, documents)

For each candidate entity, ask: "Would a future session benefit from knowing this
exists?" If yes, it's an entity.

#### Step 2: Deduplication Check

For EVERY candidate entity, run `search_nodes("entity name")` before creating it.

- **Exact match found**: Add new observations to the existing entity. Update its
  description if the current one is stale.
- **Similar match found**: Decide whether this is the same entity (→ add observations)
  or genuinely different (→ create new entity with a more specific name).
- **No match**: Create the entity with `add_entities`.

**Never skip this step.** Duplicates fragment knowledge and make search unreliable.

#### Step 3: Observation Formulation

For each entity (new or existing), extract atomic facts from this turn:

- What was said about it?
- What changed about it?
- What was decided about it?
- What was discovered about it?

Each observation = one sentence, one fact. Include dates, numbers, file paths,
and specific details. Vague observations are worthless.

#### Step 4: Relationship Mapping

For each pair of entities discussed this turn, determine if a relationship exists:

- Does entity A depend on, use, or require entity B?
- Did entity A cause, fix, or address entity B?
- Is entity A part of, or contained by, entity B?
- Did person A create, author, or approve entity B?

Create edges with `add_relationships`. Use the relationship types from conventions.md.
Set weight < 1.0 for uncertain or tentative relationships.

#### Step 5: Socratic Self-Check

Before ending the extraction pass, interrogate your work:

| Question | If "no" or "unsure"... |
|----------|----------------------|
| Did I capture every entity mentioned or implied? | Re-scan the turn for missed entities |
| Are my entity types accurate and specific? | Reclassify (e.g., `concept` → `method`) |
| Did I miss any implicit relationships? | Check if entities discussed together are connected |
| Did I store conclusions without their reasoning? | Add observations with rationale |
| Could a fresh agent reconstruct context from this? | Add more observations or fix descriptions |
| Are any existing descriptions now stale? | `update_entity` to refresh them |

This step catches the 20% of information that casual extraction misses.

## Session Start Workflow

Before diving into any task, warm-start your memory:

1. `read_graph` — Understand what's in the graph (counts, types, recent entities)
2. `search_nodes("task-relevant query")` — Find related entities
3. `get_entity("TopResult")` — Load full context with observations and relationships
4. `find_connections("KeyEntity")` if you need to understand the neighborhood

**Why:** Without recall, you start cold. Prior decisions, context, and lessons learned
are invisible. The graph IS your long-term memory.

## Session End Workflow

Before ending a session:

1. **Sweep for unstored facts** — Review what you accomplished. Anything missing?
2. **Record implementations** — If you completed planned work, create an implementation
   entity linked to the plan via `IMPLEMENTS`.
3. **Update stale descriptions** — If any entity's description no longer reflects reality,
   fix it.
4. **Final verification** — `read_graph` to confirm the graph reflects current state.

## The Plan → Implementation Loop

Every significant task should produce two linked entities:

1. **Plan** (type: `plan`) — Created before work begins
   - Observations: planned steps, goals, constraints, acceptance criteria
   - Relationships: `TARGETS` affected entities, `ADDRESSES` problems

2. **Implementation** (type: `implementation`) — Created after work completes
   - Observations: outcomes, deviations from plan, metrics, lessons learned
   - Relationships: `IMPLEMENTS` the plan, `MODIFIES` affected entities

Future sessions search for these to understand both *why* (plan) and *what happened*
(implementation).

## Duplicate Discovery

When you find two entities that represent the same thing:

1. `get_entity` on both — Review observations and relationships
2. Verify they represent the same real-world concept (not just similar names)
3. `merge_entities(source, target)` — Source is absorbed into target
4. `update_entity` on the merged entity if the description needs refinement

## Periodic Maintenance

Every few sessions, do a health check:

1. `read_graph` — Review entity counts and type distributions
2. Look for stale descriptions, orphaned entities, duplicate names
3. `delete_entities` for anything no longer relevant
4. `merge_entities` for duplicates that crept in
5. Check open plans — do any need implementations recorded?
