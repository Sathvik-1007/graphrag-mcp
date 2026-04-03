---
name: graph-mem
description: >-
  Persistent knowledge graph memory for LLM agents via Model Context Protocol.
  Stores entities, relationships, and observations in local SQLite with hybrid
  semantic + full-text search. Activates when agents need to remember facts across
  sessions, track decisions, build knowledge graphs, manage project context, or
  maintain structured long-term memory. Triggers on: remember this, store this fact,
  what do we know about, search memory, knowledge graph, graph memory, add entity,
  add observation, find connections, session context, cross-session memory, recall,
  persist knowledge, structured memory, semantic search, entity relationships.
license: MIT
metadata:
  author: Sathvik
  version: 2.0.0
  created: 2025-03-15
  last_reviewed: 2026-04-03
  review_interval_days: 30
---

# /graph-mem — Persistent Knowledge Graph Memory

You have access to a persistent, structured knowledge graph via the `graphmem-mcp`
MCP server. This memory survives across sessions. It runs entirely locally (SQLite +
embedded embeddings). No API keys required.

## The Non-Negotiable Rule

**Every turn, you MUST update the knowledge graph.** This is not optional. This is not
"when you feel like it." After you respond to the user, you extract and store entities,
observations, and relationships from the conversation. Every. Single. Turn.

If you catch yourself thinking "I'll do it later" or "this turn isn't important enough"
— that is the exact moment you must update the graph. The value of persistent memory
comes from completeness, not selectivity.

## The Double-Pass Pipeline

Every turn follows two passes:

### Pass 1: Respond to the User

Do your normal work — answer questions, write code, debug, explain. Focus entirely on
the user's request. Do not think about the graph yet.

### Pass 2: Extract and Store

After your response is complete, shift to extraction mode:

1. **Identify entities** — What people, systems, concepts, decisions, plans, problems,
   tools, or artifacts were discussed this turn? Include entities the user mentioned
   and entities you referenced.

2. **Search before creating** — For each candidate entity, run `search_nodes` to check
   if it already exists. If it does, add observations to it. If not, create it.

3. **Formulate observations** — What atomic facts were established this turn? Each
   observation is one complete sentence capturing one fact. Include dates, numbers,
   and specific details.

4. **Map relationships** — How do the entities from this turn connect to each other
   and to existing entities in the graph? Create typed, directional edges.

5. **Socratic self-check** — Before finishing, ask yourself:
   - "Did I miss any entities mentioned or implied in the conversation?"
   - "Did I assign the right entity types? Would a different type be more accurate?"
   - "Are there implicit relationships I didn't capture?"
   - "Did I store conclusions but forget the reasoning that led to them?"
   - "Would a future session be able to reconstruct the context from what I stored?"

   If any answer is "no" or "maybe," go back and fix it.

6. **Update stale descriptions** — If an entity's description no longer matches reality
   based on what was discussed, update it with `update_entity`.

## The Three Primitives

| Primitive | What It Is | Example |
|-----------|-----------|---------|
| **Entity** | A named node with type + description | `AuthService` (type: system) |
| **Observation** | An atomic fact attached to an entity | "AuthService was refactored to use JWT on 2026-03-15" |
| **Relationship** | A typed directional edge between entities | `AuthService` —DEPENDS_ON→ `PostgreSQL` |

## MCP Tools Quick Reference

### Write (10 tools)
| Tool | Purpose |
|------|---------|
| `add_entities` | Create entities (name, type, description, observations[]) |
| `add_relationships` | Create directed edges (source, target, type, weight) |
| `add_observations` | Attach facts to an existing entity |
| `update_entity` | Modify description, type, or properties |
| `update_relationship` | Change weight, type, or properties of an edge |
| `update_observation` | Edit observation text (re-embeds automatically) |
| `delete_entities` | Remove entities (cascades to obs + rels) |
| `delete_relationships` | Remove edges between entities |
| `delete_observations` | Remove specific observations by ID |
| `merge_entities` | Combine duplicates (source absorbed into target) |

### Read (8 tools)
| Tool | When to Use |
|------|-------------|
| `search_nodes` | Finding entities by concept (hybrid semantic + keyword) |
| `search_observations` | Finding specific facts in observation text |
| `get_entity` | Loading full context for one entity (obs + rels) |
| `find_connections` | Multi-hop traversal from a starting entity |
| `find_paths` | Shortest path between two entities |
| `get_subgraph` | Extract neighborhood around seed entities |
| `read_graph` | Graph overview (counts, types, most connected) |
| `list_entities` | Browse all entities with pagination |

### Multi-Graph (4 tools)
| Tool | Purpose |
|------|---------|
| `list_graphs` | Show all graphs in .graphmem/ |
| `switch_graph` | Change active graph database |
| `create_graph` | Create a new named graph |
| `delete_graph` | Remove a named graph |

## Session Lifecycle

### Session Start — Warm Up

Before doing any work, recall what you know:

```
read_graph → understand graph state (counts, types)
search_nodes("task-relevant query") → find related entities
get_entity("TopResult") → load full context
```

This prevents re-discovering things the graph already knows. A cold start is a wasted
start.

### During Session — Continuous Extraction

The double-pass pipeline runs every turn. Additionally:

- **When you make a decision**: create a decision entity with rationale as observations
- **When you discover structure**: create entities + relationships immediately
- **When a fact changes**: `update_entity` to refresh the description
- **When you find duplicates**: `merge_entities` to consolidate
- **When something becomes obsolete**: `delete_entities` to prune

### Session End — Sweep

Before ending, do a final sweep:

1. Review what you accomplished — did you store all key outcomes?
2. `add_observations` for any facts not yet stored
3. `update_entity` for any descriptions that are now stale
4. `read_graph` to verify the graph reflects current state

## Search Strategy

| Looking for... | Tool | Example query |
|----------------|------|---------------|
| Specific facts | `search_observations` | "What was the API rate limit?" |
| Entities/concepts | `search_nodes` | "authentication system" |
| How things connect | `find_connections` | Start from "AuthService" |
| Path between two things | `find_paths` | From "Bug: X" to "DatabasePool" |
| Broad overview | `get_subgraph` | Seeds: ["AuthService", "UserService"] |

## Verification Checklist

Before ending any session, verify:

- [ ] All new entities have non-empty descriptions
- [ ] Entity types are lowercase singular nouns
- [ ] Observations are atomic (one fact, complete sentence)
- [ ] Relationship types are UPPER_SNAKE_CASE verbs
- [ ] No duplicates created (searched before adding)
- [ ] Stale descriptions updated

## MCP Configuration

```json
{
  "mcpServers": {
    "graphmem-mcp": {
      "command": "graph-mem",
      "args": ["server"]
    }
  }
}
```

For a specific project: `"args": ["server", "--project-dir", "/path/to/project"]`
For a named graph: `"args": ["server", "--graph", "my-project"]`

## Reference Files

| File | Contents |
|------|----------|
| `conventions.md` | Naming standards for entities, types, relationships, observations |
| `workflows.md` | The double-pass pipeline in detail, extraction methodology |
| `best-practices.md` | Socratic self-check protocol, anti-patterns, memory hygiene |
| `domains/` | Domain-specific entity types and relationship types |
