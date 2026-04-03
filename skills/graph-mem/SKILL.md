# graph-mem: Knowledge Graph Memory

Persistent, structured knowledge graph memory for LLM agents via the Model Context Protocol.

graph-mem stores entities, relationships, and observations in a local SQLite database
with hybrid semantic + full-text search. It runs entirely locally with embedded vector
embeddings — no API keys required.

---

## What It Is

graph-mem implements **semantic memory** (entities and relationships forming a knowledge
graph) and **episodic memory** (timestamped observations capturing specific facts and events)
as defined in the CoALA cognitive architecture framework.

It is NOT working memory (your context window handles that) or procedural memory (your
training and skills handle that). It is long-term structured memory that persists across
sessions.

**This tool is domain-agnostic.** It works equally well for software engineering, academic
research, personal knowledge management, business strategy, creative projects, or any
domain where structured knowledge and cross-session continuity matter.

## Core Principle: Use It Continuously

**The graph is only useful if you maintain it.** Don't treat it as a write-once archive.
Treat it as a living document that you read from at the start of every session and write
to throughout your work.

**The ouroboros pattern**: the tool documents the work, and the work maintains the tool.
Every task has a lifecycle that should be captured in the graph:

1. **Plan** — Before starting work, store a `plan` entity describing what you intend to do
2. **Recall** — Search the graph for context, prior decisions, and related work
3. **Work + Record** — Store decisions, discoveries, and facts as you go
4. **Implement** — After completing work, store an `implementation` entity describing what was done
5. **Persist** — Sweep for anything you missed before ending the session

If you skip the plan and implementation steps, the graph becomes a disconnected collection
of facts. The plan↔implementation link is what makes the graph *navigable* — future sessions
can trace from intent to outcome and understand both the "why" and the "how."

## The Three Primitives

**Entity** — A named concept with a type and description. The node in the graph.
- Has a unique name, a type (e.g. "person", "concept", "system", "paper"), and a free-text description
- Properties dict for structured metadata

**Observation** — An atomic fact attached to an entity. Timestamped and independently searchable.
- One fact per observation: "The quarterly revenue increased 15% YoY as of Q1 2026"
- Embedded separately for fine-grained retrieval

**Relationship** — A typed, weighted, directional edge between two entities.
- Has a type (e.g. "DEPENDS_ON", "CITES", "PART_OF"), weight (0.0-1.0), and optional properties

## Core Entity Types

These entity types form the backbone of the ouroboros pattern and apply to **every domain**:

- **plan** — What you intend to do (created at session start)
- **implementation** — What you actually did (created at session end)
- **decision** — A choice that was made, with rationale as observations

Domain-specific entity types (modules, papers, people, etc.) are defined in the domain
overlay files. These three core types apply regardless of domain.

## MCP Tools

### Write Tools
- **add_entities** — Create entities (name, type, description, properties, optional observations)
- **add_relationships** — Create directed edges between entities (source → type → target)
- **add_observations** — Attach atomic facts to an existing entity
- **update_entity** — Modify description, properties, or type of an entity
- **delete_entities** — Remove entities and cascade to observations and relationships
- **merge_entities** — Absorb source entity into target, moving all data

### Read Tools
- **search_nodes** — Hybrid semantic + keyword search over entities
- **search_observations** — Search observation text directly (finds facts entity search may miss)
- **get_entity** — Full entity details including all observations and relationships
- **find_connections** — Multi-hop graph traversal from a starting entity
- **find_paths** — Shortest paths between two entities
- **get_subgraph** — Neighbourhood extraction around seed entities
- **read_graph** — Overview stats: counts, type distributions, most connected entities

## When to Use Memory

**Store** when you:
- Start a task — create a `plan` entity with steps and goals as observations
- Learn a new fact, concept, or relationship
- Make or discover a decision and its rationale
- Encounter an important person, system, paper, or artifact
- Complete a task — create an `implementation` entity linked to the plan
- Discover a problem, its root cause, and resolution

**Retrieve** when you:
- Start a new task or session (warm-start with context)
- Need to make a decision (check for prior decisions and context)
- Encounter something that might already be known
- Need to understand how things relate to each other
- Want to understand *why* something was done a certain way (search for plans)

**Update** when:
- Facts change or descriptions become stale
- Entities should be merged (duplicates discovered)
- Observations need correction

**Forget** (delete) when:
- Information is confirmed wrong or obsolete
- Entities are no longer relevant

## MCP Configuration

```json
{
  "mcpServers": {
    "graph-mem": {
      "command": "uvx",
      "args": ["graph-mem", "server"]
    }
  }
}
```
