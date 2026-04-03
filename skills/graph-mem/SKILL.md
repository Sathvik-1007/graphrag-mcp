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

# /graph-mem — Knowledge Graph Memory for Agents

You are an agent with access to persistent, structured knowledge graph memory via
the `graphmem-mcp` MCP server. This memory survives across sessions. Use it to store
entities, relationships, and observations — and to recall them when you need context.

The graph runs entirely locally (SQLite + embedded embeddings). No API keys required.

## When This Skill Activates

Use graph-mem tools whenever you need to:
- **Remember** facts, decisions, people, systems, or concepts across sessions
- **Recall** prior context before starting new work
- **Track** plans, implementations, and their outcomes
- **Search** for related knowledge using natural language
- **Navigate** entity relationships and find connections
- **Maintain** a living knowledge base that grows with each session

## The Three Primitives

| Primitive | What It Is | Example |
|-----------|-----------|---------|
| **Entity** | A named node with type + description | `Harry Potter` (type: person) |
| **Observation** | An atomic fact attached to an entity | "Harry received his Hogwarts letter on his 11th birthday" |
| **Relationship** | A typed directional edge between entities | `Harry Potter` —ATTENDS→ `Hogwarts` |

## MCP Tools Reference

### Write Tools
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `add_entities` | Create entities | name, entity_type, description, observations[] |
| `add_relationships` | Create edges | source, target, relationship_type, weight |
| `add_observations` | Attach facts to entity | entity_name, observations[] |
| `update_entity` | Modify entity fields | name, description, entity_type, properties |
| `delete_entities` | Remove entities (cascades) | names[] |
| `merge_entities` | Combine two entities | source → target |

### Read Tools
| Tool | Purpose | When to Use |
|------|---------|-------------|
| `search_nodes` | Hybrid semantic + keyword search | Finding entities by concept |
| `search_observations` | Search observation text | Finding specific facts |
| `get_entity` | Full entity with obs + rels | Loading complete context |
| `find_connections` | Multi-hop graph traversal | Exploring neighborhoods |
| `find_paths` | Shortest paths between entities | Understanding relationships |
| `get_subgraph` | Extract neighborhood | Visualizing local graph |
| `read_graph` | Overview stats | Health checks, orientation |
| `list_entities` | Browse with pagination | Discovering graph contents |

### Multi-Graph Tools
| Tool | Purpose |
|------|---------|
| `list_graphs` | Show all named graphs in .graphmem/ |
| `switch_graph` | Switch active graph database |
| `create_graph` | Create a new named graph |
| `delete_graph` | Remove a named graph |

## Core Workflow: The Ouroboros Pattern

The graph documents the work, and the work maintains the graph. Every session follows
this lifecycle:

### 1. Recall (Session Start)
```
read_graph → understand what's in the graph
search_nodes("relevant query") → find related entities
get_entity("EntityName") → load full context
```

### 2. Plan (Before Work)
```
add_entities([{name: "Plan: Task Name", entity_type: "plan", description: "..."}])
add_observations("Plan: Task Name", ["Step 1: ...", "Step 2: ...", "Goal: ..."])
add_relationships([{source: "Plan: Task Name", target: "AffectedEntity", type: "TARGETS"}])
```

### 3. Work + Record (During Work)
Store decisions, discoveries, and facts **as you go** — not at the end:
```
add_entities([{name: "Decision: Use X over Y", entity_type: "decision", ...}])
add_observations("ExistingEntity", ["New fact discovered during work"])
add_relationships([{source: "NewThing", target: "ExistingThing", type: "DEPENDS_ON"}])
```

### 4. Implement (Session End)
```
add_entities([{name: "Implementation: Task Name", entity_type: "implementation", ...}])
add_relationships([{source: "Implementation: Task Name", target: "Plan: Task Name", type: "IMPLEMENTS"}])
```

### 5. Verify
```
read_graph → confirm graph reflects current state
get_entity("Plan: Task Name") → check all steps tracked
```

## Verification Checklist

Before ending any session where you used graph-mem, verify:

- [ ] All new entities have descriptions (not empty)
- [ ] Entity types are lowercase singular nouns (person, concept, system, decision, plan)
- [ ] Observations are atomic (one fact each, complete sentences)
- [ ] Relationship types are UPPER_SNAKE_CASE verbs (DEPENDS_ON, IMPLEMENTS, TARGETS)
- [ ] No duplicate entities created (searched before adding)
- [ ] Plans have corresponding implementations (or note "in progress")
- [ ] Stale descriptions updated if facts changed

## Naming Conventions

**Entity names**: Descriptive, natural, searchable
- Systems: `AuthService`, `DatabasePool` (PascalCase)
- People: `Alice Johnson`, `Dr. Smith` (natural names)
- Plans: `Plan: Implement Auth Service`
- Decisions: `Decision: Use PostgreSQL`

**Entity types**: Lowercase, singular nouns
- `person`, `concept`, `system`, `decision`, `plan`, `implementation`, `problem`

**Relationship types**: UPPER_SNAKE_CASE verb phrases (source → target direction)
- `DEPENDS_ON`, `IMPLEMENTS`, `TARGETS`, `PART_OF`, `USES`, `CITES`

**Observations**: Complete sentences, one atomic fact each
- Good: "The API rate limit was increased from 100 to 500 req/s on 2026-03-15"
- Bad: "rate limit stuff changed" / "changed AND deployed"

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Batch writes at session end | You'll forget details | Write as you go |
| Plans without implementations | Loses outcome context | Always record what happened |
| Empty descriptions | Unsearchable entities | Write meaningful summaries |
| Multiple facts per observation | Can't search individually | One fact = one observation |
| Skip search, create duplicate | Fragments knowledge | Always search_nodes first |
| Store raw content dumps | Noise overwhelms signal | Store facts *about* content |
| Never update/delete | Graph becomes stale | Maintain actively |

## Multi-Graph Usage

graph-mem supports multiple named graphs stored as separate `.db` files in
`~/.graphmem/`. Use this to keep different knowledge domains separate:

```
create_graph("project-alpha")    → creates ~/.graphmem/project-alpha.db
switch_graph("project-alpha")    → switches all tools to use this graph
list_graphs()                    → shows all graphs with entity/rel/obs counts
delete_graph("old-project")      → removes the graph file
```

The `--graph` CLI flag also selects graphs: `graph-mem server --graph project-alpha`

## Search Strategy

| Looking for... | Use this tool | Example |
|----------------|--------------|---------|
| Specific facts | `search_observations` | "What was the API rate limit?" |
| Entities/concepts | `search_nodes` | "authentication system" |
| How things connect | `find_connections` | Starting from "AuthService" |
| Path between two things | `find_paths` | From "Bug: Memory Leak" to "DatabasePool" |
| Broad overview | `get_subgraph` | Seed: ["AuthService", "UserService"] |
| Prior work | `search_nodes` | "Plan: feature name" |

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

For a specific graph: `"args": ["server", "--graph", "my-project"]`

For pip-installed: `"command": "graph-mem"` (after `pip install graph-mem`)
For uvx: `"command": "uvx"`, `"args": ["graph-mem", "server"]`

## Reference Files

| File | Contents |
|------|----------|
| `best-practices.md` | The ouroboros pattern, memory hygiene, granularity guidelines |
| `conventions.md` | Naming standards for entities, types, relationships, observations |
| `workflows.md` | Session start/during/end workflows, search strategy, maintenance |
| `domains/` | Domain-specific overlays (software engineering, research, etc.) |
