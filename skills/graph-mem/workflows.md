# Workflows

## Session Start — Recall & Plan

Before diving into any task, warm-start your memory and store the plan:

### Step 1: Recall what you know

1. `read_graph` — Understand what's in the graph (counts, types, recent entities)
2. `search_nodes` with a task-relevant query — Find related entities
3. `get_entity` on top results — Load full context with observations and relationships
4. `find_connections` if you need to understand how things relate — Explore the neighbourhood

**Why this matters:** Without recall, you start every session cold. Prior decisions,
context, and lessons learned are lost. The graph is your long-term memory — use it.

### Step 2: Store the plan

Before doing any work, store your plan in the graph:

1. `add_entities` — Create a plan entity:
   - **name**: Descriptive name (e.g. "Plan: Redesign Search Pipeline", "Plan: Literature Review on Transformer Architectures", "Plan: Quarterly Strategy Analysis")
   - **type**: `plan`
   - **description**: One-paragraph summary of what you intend to do and why
2. `add_observations` on the plan entity — One observation per planned step or goal:
   - "Step 1: Identify all papers citing the original attention paper from 2017"
   - "Step 2: Categorize by approach — sparse attention, linear attention, hybrid"
   - "Goal: Produce a comparison table with strengths and weaknesses"
   - "Constraint: Focus on papers from 2023-2026 only"
3. `add_relationships` — Link the plan to related entities:
   - `plan TARGETS entity` — What the plan will examine or modify
   - `plan FOLLOWS_FROM decision` — What decision led to this plan
   - `plan ADDRESSES problem` — What problem this plan solves

**Why store the plan?** Future sessions can search for plans to understand *why* work
was done. Plans also serve as acceptance criteria — at session end, compare what you
did against what you planned.

## During Work — Continuous Memory

As you work, maintain the graph. Don't batch everything to the end — update as you go:

### When to store (do this immediately, not later)

- **You make a decision** → `add_entities` with type `decision`, include rationale as an observation
- **You discover structure** → `add_entities` for the concept + `add_relationships` for connections
- **You learn a new fact** → `add_observations` on the relevant entity
- **You encounter a problem** → `add_entities` with type `problem`, add root cause and resolution as observations
- **You complete a milestone** → `add_observations` on the plan entity ("Completed: Step 2 — categorized 47 papers")
- **You deviate from the plan** → `add_observations` on the plan entity explaining why and what changed

### When to update

- **A fact changes** → `update_entity` to refresh the description
- **You find duplicates** → `merge_entities` to consolidate
- **Something becomes obsolete** → `delete_entities` to prune

### The 5-minute rule

If you've been working for more than 5 minutes without touching the graph, pause and ask:
"Did I learn anything worth remembering?" If yes, store it now. If you wait until the end
of the session, you'll forget details or skip it entirely.

## Session End — Persist & Record Implementation

Before ending a session, do a memory sweep and record what was actually done:

### Step 1: Sweep for unstored facts

1. Review what you accomplished — what decisions were made? What did you learn?
2. `add_observations` for any facts not yet stored
3. `update_entity` for any descriptions that are now stale

### Step 2: Record the implementation

Store the implementation result alongside the plan:

1. `add_entities` — Create an implementation entity:
   - **name**: Match the plan name (e.g. "Implementation: Redesign Search Pipeline")
   - **type**: `implementation`
   - **description**: Summary of what was actually done, including any deviations from the plan
2. `add_observations` on the implementation entity — Key outcomes:
   - "Reviewed 47 papers on efficient attention mechanisms from 2023-2026"
   - "Produced comparison table covering 6 categories of approaches"
   - "Key finding: linear attention methods sacrifice quality for speed in long-context scenarios"
   - "Deviated from plan: expanded scope to include 2022 papers that introduced key techniques"
3. `add_relationships` — Link implementation to plan and affected entities:
   - `implementation IMPLEMENTS plan` — Links what was done to what was planned
   - `implementation MODIFIES entity` — What was changed or enriched
   - `implementation INTRODUCES entity` — New entities discovered during work

### Step 3: Final verification

1. `read_graph` to verify the graph reflects current state
2. Check that the plan entity has observations tracking completion of each step
3. Verify key decisions are stored with rationale

**The plan↔implementation loop** is the ouroboros pattern: future sessions search for
plans to understand intent and implementations to understand what happened. Without
both, you only get half the picture.

## After Learning Something — Store

When you discover important information worth remembering:

1. Identify new entities, observations, and relationships from the session
2. `search_nodes` to check if entities already exist — Avoid creating duplicates
3. `add_entities` for genuinely new concepts (include description and type)
4. `add_observations` to attach new facts to existing or new entities
5. `add_relationships` to connect entities with typed, directional edges

## Duplicate Discovery — Merge

When you find two entities that represent the same thing:

1. `get_entity` on both candidates — Review their observations and relationships
2. Verify they represent the same real-world concept (not just similar names)
3. `merge_entities` — Source is absorbed into target (all data moves to target)
4. `update_entity` on the merged entity if the description needs refinement

## Search Strategy

For **specific facts** (dates, numbers, exact events):
- Use `search_observations` — It searches observation text directly

For **concepts and entities** (people, systems, decisions, papers):
- Use `search_nodes` — It searches entity names, types, and descriptions, boosted by matching observations

For **relationships and structure** (how things connect):
- Start with `search_nodes` or `get_entity`, then use `find_connections` or `find_paths`

For **broad overview** (what do we know about X):
- Use `get_subgraph` with seed entities to extract a neighbourhood

For **prior plans and implementations** (what was intended vs what happened):
- `search_nodes` with query like "Plan: feature name" or "Implementation: feature name"
- Compare plan observations against implementation observations to understand deviations

## Periodic Maintenance

Every few sessions, do a health check:

1. `read_graph` — Review entity counts and type distributions
2. Look for stale entities with outdated descriptions
3. Look for orphaned entities with no relationships
4. `delete_entities` for anything no longer relevant
5. `merge_entities` for any duplicates that crept in
6. Review open plans — do any need implementations recorded?
