# Workflows

## Recall Workflow (Session Start)

Before diving into any task, warm-start your memory:

1. `read_graph` — Understand what's in the graph (counts, types, recent entities)
2. `search_nodes` with a task-relevant query — Find related entities
3. `get_entity` on top results — Load full context with observations and relationships
4. `find_connections` if you need to understand how things relate — Explore the neighbourhood

## Store Workflow (After Learning Something)

When you discover important information worth remembering:

1. Identify new entities, observations, and relationships from the session
2. `search_nodes` to check if entities already exist — Avoid creating duplicates
3. `add_entities` for genuinely new concepts (include description and type)
4. `add_observations` to attach new facts to existing or new entities
5. `add_relationships` to connect entities with typed, directional edges

## Merge Workflow (Duplicate Discovery)

When you find two entities that represent the same thing:

1. `get_entity` on both candidates — Review their observations and relationships
2. Verify they represent the same real-world concept (not just similar names)
3. `merge_entities` — Source is absorbed into target (all data moves to target)
4. `update_entity` on the merged entity if the description needs refinement

## Search Strategy

For **specific facts** (dates, numbers, exact events):
- Use `search_observations` — It searches observation text directly

For **concepts and entities** (people, systems, decisions):
- Use `search_nodes` — It searches entity names, types, and descriptions, boosted by matching observations

For **relationships and structure** (how things connect):
- Start with `search_nodes` or `get_entity`, then use `find_connections` or `find_paths`

For **broad overview** (what do we know about X):
- Use `get_subgraph` with seed entities to extract a neighbourhood
