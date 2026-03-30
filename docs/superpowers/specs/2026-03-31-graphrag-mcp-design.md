# graphrag-mcp: Production-Grade Graph-RAG MCP Server

**Date**: 2026-03-31
**Status**: Design
**Quality bar**: Publishable OSS, zero errors, no hardcoding, no simplification

---

## 1. Problem Statement

LLM-powered CLI agents (Claude Code, Codex, Gemini CLI, OpenCode, Cursor, etc.) lack persistent, structured memory across sessions. When working on complex projects -- novels, documentaries, large codebases, research -- context is lost between sessions. Side characters are forgotten, architectural decisions drift, research connections are missed.

Existing solutions (Cognee, LightRAG, knowledge-mcp) all require external API keys or cloud services, making them unsuitable for local-first, privacy-conscious workflows.

## 2. Solution

**graphrag-mcp** is a production-grade MCP server that provides any LLM-powered CLI agent with a persistent, per-project knowledge graph combining:

- **Graph storage**: Entities, relationships, and observations in a structured graph
- **Semantic search**: Vector similarity search over entity descriptions and observations using local embeddings (no API keys)
- **Multi-hop traversal**: Recursive graph traversal to find deep connections
- **Combined retrieval**: Query planner that fuses semantic + structural results

The agent itself is the intelligence -- it decides what entities/relationships to create and when to query the graph. The server is the storage and retrieval engine.

## 3. Architecture

```
┌─────────────────────────────────────────────────────┐
│  CLI Agent (Claude Code / Codex / Gemini / OpenCode)│
│  Uses MCP tools to read/write the knowledge graph   │
└──────────────────┬──────────────────────────────────┘
                   │ MCP Protocol (stdio / SSE)
┌──────────────────▼──────────────────────────────────┐
│  graphrag-mcp server (Python, FastMCP)              │
│                                                     │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐  │
│  │ Graph       │ │ Semantic    │ │ Query        │  │
│  │ Engine      │ │ Engine      │ │ Planner      │  │
│  │             │ │             │ │              │  │
│  │ • entities  │ │ • embed()   │ │ • fuse graph │  │
│  │ • edges     │ │ • search()  │ │   + semantic │  │
│  │ • traverse  │ │ • batch()   │ │ • rank       │  │
│  │ • subgraph  │ │ • cache     │ │ • deduplicate│  │
│  └──────┬──────┘ └──────┬──────┘ └──────┬───────┘  │
│         └───────┬───────┘               │           │
│         ┌───────▼───────────────────────▼────────┐  │
│         │  SQLite + sqlite-vec (per-project)     │  │
│         │  .graphrag/graph.db                    │  │
│         └────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  graphrag-mcp CLI                                   │
│  install <agent> │ init │ status │ export │ import  │
└─────────────────────────────────────────────────────┘
```

### 3.1 Why SQLite + sqlite-vec (not Neo4j)

- **Embedded**: Zero config, no server process, no JVM, no credentials
- **Single file**: `.graphrag/graph.db` per project -- portable, backupable
- **Distribution**: `pip install graphrag-mcp` and done
- **Memory efficient**: Memory-mapped I/O, no resident server process eating RAM
- **Fast enough**: At per-project scale (hundreds to low thousands of entities), recursive CTEs with proper indexing handle multi-hop traversal in <10ms
- **WAL mode**: Concurrent reads, single writer -- perfect for MCP server usage pattern

Neo4j requires JVM + a running server process (1-2GB RAM minimum), making it unsuitable for a CLI tool that should "just work" after pip install.

### 3.2 Why local embeddings (not API keys)

- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (default, 22MB, 384-dim) or configurable
- **ONNX runtime**: CPU-only inference, ~5-15ms per embedding, minimal RAM (~100MB model loaded)
- **Lazy loading**: Model loads on first semantic operation, not at server start
- **Embedding cache**: SHA-256 content hash → embedding, avoids recomputing for unchanged content
- **Fallback**: If model fails to load, graph operations still work -- semantic search gracefully degrades with a clear warning

Note: `all-MiniLM-L6-v2` chosen over `embeddinggemma-300m` as default because it's 22MB vs ~1.2GB, loads faster, uses less RAM, and has excellent quality for short-text similarity. Users can configure any sentence-transformers model via `GRAPHRAG_EMBEDDING_MODEL` env var.

## 4. Database Schema

```sql
-- Schema version tracking for migrations
CREATE TABLE schema_version (
    version INTEGER PRIMARY KEY,
    applied_at REAL NOT NULL,
    description TEXT NOT NULL
);

-- Core entity table
CREATE TABLE entities (
    id TEXT PRIMARY KEY,          -- ULID for sortable unique IDs
    name TEXT NOT NULL,
    entity_type TEXT NOT NULL,    -- person, place, concept, event, decision, etc.
    description TEXT,             -- rich description, also used for embedding
    properties TEXT,              -- JSON object for arbitrary key-value pairs
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

-- Unique constraint on (name, entity_type) to prevent accidental duplicates
CREATE UNIQUE INDEX idx_entities_name_type ON entities(name, entity_type);
CREATE INDEX idx_entities_type ON entities(entity_type);
CREATE INDEX idx_entities_updated ON entities(updated_at);

-- Relationships (directed edges)
CREATE TABLE relationships (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    target_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL,
    weight REAL NOT NULL DEFAULT 1.0,   -- strength/confidence
    properties TEXT,                     -- JSON
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

CREATE UNIQUE INDEX idx_rel_source_target_type
    ON relationships(source_id, target_id, relationship_type);
CREATE INDEX idx_rel_target ON relationships(target_id);
CREATE INDEX idx_rel_type ON relationships(relationship_type);

-- Observations: factual statements attached to entities
CREATE TABLE observations (
    id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    source TEXT,                  -- provenance (session ID, document, user input)
    created_at REAL NOT NULL
);

CREATE INDEX idx_obs_entity ON observations(entity_id);

-- Vector embeddings for entities (description + name)
-- Dimension is auto-detected from the configured model at init time
CREATE VIRTUAL TABLE entity_embeddings USING vec0(
    id TEXT PRIMARY KEY,
    embedding float[{dim}]
);

-- Vector embeddings for observations
CREATE VIRTUAL TABLE observation_embeddings USING vec0(
    id TEXT PRIMARY KEY,
    embedding float[{dim}]
);

-- Embedding cache: avoid recomputing embeddings for unchanged content
CREATE TABLE embedding_cache (
    content_hash TEXT PRIMARY KEY,    -- SHA-256 of input text
    embedding BLOB NOT NULL,          -- raw float array
    model_name TEXT NOT NULL,         -- model that produced this
    created_at REAL NOT NULL
);

-- Full-text search on entity names and descriptions
CREATE VIRTUAL TABLE entities_fts USING fts5(
    name, description, entity_type,
    content=entities, content_rowid=rowid
);

-- Full-text search on observations
CREATE VIRTUAL TABLE observations_fts USING fts5(
    content,
    content=observations, content_rowid=rowid
);
```

### 4.1 Schema Migrations

Every schema change gets a numbered migration in `src/graphrag_mcp/db/migrations/`. On startup, the server checks `schema_version` and applies any pending migrations in order. Migrations are Python functions (not raw SQL files) so they can do data transforms.

## 5. MCP Tools

### 5.1 Write Tools

**`add_entities`** — Batch-create entities
```json
{
    "entities": [
        {
            "name": "John Smith",
            "entity_type": "person",
            "description": "Protagonist, a retired detective living in Berlin",
            "properties": {"age": 52, "occupation": "retired detective"},
            "observations": [
                "Has a limp from a childhood injury",
                "Speaks fluent German and English"
            ]
        }
    ]
}
```
- Validates entity types against configurable type registry
- On name+type conflict: **merges** by appending description and observations (not fail, not overwrite)
- Returns created/merged entity IDs with status

**`add_relationships`** — Batch-create relationships
```json
{
    "relationships": [
        {
            "source": "John Smith",
            "target": "Berlin",
            "relationship_type": "lives_in",
            "weight": 1.0,
            "properties": {"since": "2019"}
        }
    ]
}
```
- Resolves entities by name (fuzzy match if exact not found)
- On duplicate (same source+target+type): updates weight and properties
- Returns created/updated relationship IDs

**`add_observations`** — Add factual statements to existing entities
```json
{
    "entity_name": "John Smith",
    "observations": [
        "Received a mysterious letter in Chapter 3",
        "His ex-wife Maria called him on Tuesday"
    ],
    "source": "chapter-3-review"
}
```

**`update_entity`** — Modify entity description or properties
**`delete_entities`** — Remove entities (cascades to relationships and observations)
**`merge_entities`** — Merge two entities into one (combine observations, redirect relationships)

### 5.2 Read Tools

**`search_nodes`** — Semantic + full-text hybrid search
```json
{
    "query": "characters with connections to Berlin",
    "limit": 10,
    "entity_types": ["person"],        // optional filter
    "include_observations": true
}
```
- Runs both vector similarity AND FTS5 full-text search
- Fuses results using Reciprocal Rank Fusion (RRF)
- Returns entities with relevance scores, their observations, and direct relationships

**`find_connections`** — Multi-hop graph traversal
```json
{
    "entity_name": "John Smith",
    "max_hops": 3,
    "relationship_types": ["knows", "lives_in"],  // optional filter
    "direction": "both"                            // outgoing, incoming, both
}
```
- Uses recursive CTE with cycle detection and depth tracking
- Returns the subgraph of all reachable entities within max_hops
- Each result includes the path (chain of relationships) that connects it

**`get_entity`** — Full details of a single entity
- All properties, all observations, all direct relationships (in and out)

**`read_graph`** — Graph overview and statistics
- Total entities, relationships, observations
- Entity type distribution
- Most connected entities (by degree)
- Relationship type distribution
- Recent additions

**`get_subgraph`** — Extract a neighborhood around multiple seed entities
```json
{
    "entity_names": ["John Smith", "Maria", "Berlin"],
    "radius": 2
}
```
- BFS from each seed entity up to radius hops
- Returns the union subgraph: all entities and relationships in the neighborhood
- Useful for getting full context around a set of related concepts

**`find_paths`** — Shortest path between two entities
```json
{
    "source": "John Smith",
    "target": "The Organization",
    "max_hops": 5
}
```
- BFS shortest path with cycle prevention
- Returns the path as a chain of entities and relationships

### 5.3 Tool Design Principles

- **Batch-first**: Write tools accept arrays, not single items. Reduces round-trips.
- **Name-based resolution**: Tools accept entity names (human-readable), not IDs. The server resolves names to IDs internally, with fuzzy matching as fallback.
- **Merge-on-conflict**: Creating an entity that already exists merges information rather than failing. The graph should grow, not break.
- **Cascading deletes**: Removing an entity removes its relationships and observations. No orphaned edges.
- **Configurable defaults**: Limits, entity types, relationship types all configurable.

## 6. Semantic Engine

### 6.1 Embedding Pipeline

```
Input text → SHA-256 hash → Cache lookup
  ├── Cache hit → Return cached embedding
  └── Cache miss → Model inference → Cache store → Return embedding
```

- **Model loading**: Lazy-loaded on first use. Uses `sentence-transformers` with ONNX backend when available.
- **ONNX optimization**: If `onnxruntime` is installed, automatically uses ONNX for ~3x faster inference and lower memory.
- **Batch embedding**: When inserting multiple entities/observations, embeddings are computed in a single batch call.
- **Dimension auto-detection**: On first model load, compute a test embedding to detect dimensionality. Store in schema metadata. Refuse to mix models with different dimensions in the same database.

### 6.2 Search Strategy

Hybrid search combining:
1. **Vector similarity** (cosine distance via sqlite-vec): Good for semantic meaning
2. **FTS5 full-text** (BM25 ranking): Good for exact term matches
3. **Reciprocal Rank Fusion (RRF)**: Combines rankings from both methods

```
RRF_score(entity) = Σ 1 / (k + rank_in_method)
```
where k=60 (standard constant). This avoids the need to normalize scores across methods.

## 7. Graph Engine

### 7.1 Traversal

Multi-hop traversal using recursive CTEs with:
- **Cycle detection**: Track visited set in CTE, skip already-seen entities
- **Depth tracking**: Each row carries its depth, stop at max_hops
- **Direction filtering**: Follow outgoing, incoming, or both relationship directions
- **Relationship type filtering**: Optionally restrict to specific relationship types
- **Path reconstruction**: Each result carries the full path from the seed entity

### 7.2 Entity Resolution

When tools receive entity names (strings), the server resolves them:
1. **Exact match** on `(name, entity_type)` if type provided
2. **Exact match** on `name` (case-insensitive) across all types
3. **FTS5 match** on name for partial/fuzzy matches
4. **Vector similarity** on name+description for semantic matches
5. If no match found, return an error with suggestions of similar entities

This cascade ensures robust resolution without requiring users to remember exact names.

### 7.3 Entity Merge

When merging two entities (A absorbs B):
1. Append B's description to A's description
2. Move all of B's observations to A
3. Redirect all of B's relationships to A (both source and target references)
4. Handle duplicate relationships (same source+target+type after redirect) by keeping the higher-weight one
5. Delete B
6. Recompute A's embedding
7. All in a single transaction

## 8. CLI

```bash
# MCP server (primary use)
graphrag-mcp server                      # stdio transport (default)
graphrag-mcp server --transport sse      # SSE transport for remote
graphrag-mcp server --transport streamable-http
graphrag-mcp server --db /path/to/graph.db  # explicit database path

# Agent skill installation (desloppify pattern)
graphrag-mcp install claude              # Writes to ~/.claude/skills/graphrag-mcp/
graphrag-mcp install codex               # Writes to ~/.codex/AGENTS.md (section)
graphrag-mcp install gemini              # Writes to AGENTS.md (section)
graphrag-mcp install opencode            # Writes to ~/.config/opencode/skills/graphrag-mcp/
graphrag-mcp install cursor              # Writes to .cursor/rules/graphrag-mcp.md
graphrag-mcp install --global claude     # Global install (user-level)
graphrag-mcp install --project claude    # Project-level install

# Graph management
graphrag-mcp init                        # Create .graphrag/ in current directory
graphrag-mcp status                      # Graph statistics
graphrag-mcp export --format json        # Export graph (json, graphml, csv)
graphrag-mcp import graph.json           # Import from file
graphrag-mcp validate                    # Check database integrity
```

### 8.1 Install Targets

Following the desloppify pattern, each agent has known skill/config locations:

| Agent     | Project-level path                          | Global path                                    | Method        |
|-----------|---------------------------------------------|------------------------------------------------|---------------|
| claude    | `.claude/skills/graphrag-mcp/SKILL.md`      | `~/.claude/skills/graphrag-mcp/SKILL.md`       | Overwrite     |
| opencode  | `.opencode/skills/graphrag-mcp/SKILL.md`    | `~/.config/opencode/skills/graphrag-mcp/SKILL.md` | Overwrite  |
| codex     | `.agents/skills/graphrag-mcp/SKILL.md`      | `~/.codex/AGENTS.md`                           | Section       |
| gemini    | `AGENTS.md`                                 | `~/.gemini/skills/graphrag-mcp/SKILL.md`       | Section/Overwrite |
| cursor    | `.cursor/rules/graphrag-mcp.md`             | N/A                                            | Overwrite     |
| windsurf  | `AGENTS.md`                                 | N/A                                            | Section       |
| amp       | `.agents/skills/graphrag-mcp/SKILL.md`      | `~/.config/agents/skills/graphrag-mcp/SKILL.md` | Overwrite   |

"Section" method uses `<!-- graphrag-mcp-begin -->` / `<!-- graphrag-mcp-end -->` markers for safe section replacement in shared files (like AGENTS.md).

## 9. SKILL.md

The skill document installed by `graphrag-mcp install <agent>` instructs agents on:

1. **When to add entities**: Whenever encountering important concepts, people, places, events, decisions, patterns, or anything that might be referenced later
2. **When to search**: At session start to load relevant context, when a topic comes up that might have prior knowledge, when the user references something from a previous session
3. **How to maintain**: Update descriptions when learning new info, merge duplicates, add observations as new facts emerge
4. **Entity type guidance**: Flexible types (person, place, concept, event, decision, code_component, etc.) -- not a fixed ontology, but examples and conventions
5. **Relationship conventions**: Common relationship types with directionality guidance (lives_in, knows, causes, part_of, depends_on, contradicts, etc.)

The skill also includes the MCP server configuration snippet for the agent to auto-register if not already configured.

## 10. Configuration

All configurable via environment variables (12-factor app style):

| Variable                        | Default                          | Description                          |
|---------------------------------|----------------------------------|--------------------------------------|
| `GRAPHRAG_DB_PATH`              | `.graphrag/graph.db`             | Database file path                   |
| `GRAPHRAG_EMBEDDING_MODEL`      | `all-MiniLM-L6-v2`              | sentence-transformers model name     |
| `GRAPHRAG_USE_ONNX`             | `true`                           | Use ONNX runtime if available        |
| `GRAPHRAG_EMBEDDING_DEVICE`     | `cpu`                            | Inference device (cpu/cuda)          |
| `GRAPHRAG_CACHE_SIZE`           | `10000`                          | Embedding cache max entries          |
| `GRAPHRAG_SEARCH_LIMIT`         | `10`                             | Default search result limit          |
| `GRAPHRAG_MAX_HOPS`             | `4`                              | Default max traversal depth          |
| `GRAPHRAG_LOG_LEVEL`            | `WARNING`                        | Logging verbosity                    |
| `GRAPHRAG_TRANSPORT`            | `stdio`                          | MCP transport (stdio/sse/streamable-http) |

## 11. Project Structure

```
graphrag-mcp/
├── pyproject.toml                       # Project metadata, dependencies, entry points
├── README.md                            # Paste-into-agent install prompt + docs
├── LICENSE                              # MIT
├── CLAUDE.md                            # Development guide for Claude Code contributors
├── AGENTS.md                            # Development guide for other agents
├── .gitignore
├── src/
│   └── graphrag_mcp/
│       ├── __init__.py                  # Package version, public API
│       ├── __main__.py                  # python -m graphrag_mcp entry point
│       ├── server.py                    # FastMCP server setup, tool registration
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py                  # Click CLI group (server, install, init, status, export, import)
│       │   └── install.py               # Agent-specific skill installation logic
│       ├── db/
│       │   ├── __init__.py
│       │   ├── connection.py            # Connection pool, WAL setup, async wrapper
│       │   ├── schema.py                # Schema creation, migration runner
│       │   └── migrations/
│       │       ├── __init__.py
│       │       ├── v001_initial.py      # Initial schema
│       │       └── ...
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── engine.py                # CRUD operations for entities, relationships, observations
│       │   ├── traversal.py             # Multi-hop traversal, shortest path, subgraph extraction
│       │   └── merge.py                 # Entity deduplication and merge logic
│       ├── semantic/
│       │   ├── __init__.py
│       │   ├── embeddings.py            # Model loading (lazy), ONNX detection, batch embed
│       │   └── search.py                # Hybrid search (vector + FTS5 + RRF fusion)
│       ├── models/
│       │   ├── __init__.py
│       │   ├── entity.py                # Entity dataclass + validation
│       │   ├── relationship.py          # Relationship dataclass + validation
│       │   └── observation.py           # Observation dataclass + validation
│       └── utils/
│           ├── __init__.py
│           ├── config.py                # Env-var-based configuration with validation
│           ├── ids.py                   # ULID generation
│           ├── logging.py               # Structured logging setup
│           └── errors.py                # Custom exception hierarchy
├── tests/
│   ├── conftest.py                      # Shared fixtures (temp DB, sample data)
│   ├── test_graph/
│   │   ├── test_engine.py
│   │   ├── test_traversal.py
│   │   └── test_merge.py
│   ├── test_semantic/
│   │   ├── test_embeddings.py
│   │   └── test_search.py
│   ├── test_server/
│   │   └── test_tools.py
│   ├── test_cli/
│   │   ├── test_install.py
│   │   └── test_commands.py
│   └── test_db/
│       ├── test_connection.py
│       └── test_migrations.py
└── skills/
    └── SKILL.md                         # Base skill document for all agents
```

## 12. Dependencies

### Core (required)
- `mcp>=1.0` — MCP SDK (FastMCP)
- `sqlite-vec>=0.1` — Vector search extension for SQLite
- `sentence-transformers>=2.0` — Local embedding models
- `click>=8.0` — CLI framework
- `ulid-py>=2.0` — Sortable unique IDs

### Optional (for performance)
- `onnxruntime>=1.15` — ONNX backend for faster embeddings (auto-detected)

### Development
- `pytest>=7.0`
- `pytest-asyncio`
- `ruff` — Linting + formatting
- `mypy` — Type checking

## 13. Error Handling Strategy

Custom exception hierarchy rooted at `GraphRAGError`:

```
GraphRAGError
├── DatabaseError          — SQLite connection/query failures
│   ├── SchemaError        — Migration or schema issues
│   └── IntegrityError     — Constraint violations
├── EntityError            — Entity operations
│   ├── EntityNotFound     — Name resolution failed
│   └── DuplicateEntity    — Merge conflict that can't be auto-resolved
├── RelationshipError      — Edge operations
├── EmbeddingError         — Model loading or inference failures
│   ├── ModelLoadError     — Model not found or can't load
│   └── DimensionMismatch  — Embedding dimension doesn't match DB
├── SearchError            — Query execution failures
├── ConfigError            — Invalid configuration
└── ExportError            — Import/export failures
```

Every MCP tool wraps its logic in proper error handling and returns structured error responses (not stack traces) to the agent. Errors include actionable suggestions (e.g., "Entity 'Jon Smith' not found. Did you mean 'John Smith'?").

## 14. Performance Considerations

- **Connection pooling**: Reuse SQLite connections with proper cleanup
- **WAL mode**: Write-ahead logging for concurrent reads during writes
- **Prepared statements**: Parameterized queries, no string concatenation
- **Batch operations**: All write tools accept arrays, use single transactions
- **Embedding cache**: Content-hash-based cache avoids recomputing unchanged embeddings
- **Lazy model loading**: Embedding model loads only on first semantic operation
- **ONNX auto-detection**: Uses ONNX runtime when installed for ~3x faster inference
- **Memory-mapped I/O**: SQLite uses mmap for efficient large-database access
- **Index coverage**: Every query path has a supporting index
- **PRAGMA tuning**: journal_mode=WAL, synchronous=NORMAL, cache_size=64MB, mmap_size=256MB
- **FTS5 triggers**: Keep full-text indexes in sync with base tables via triggers

## 15. Testing Strategy

- **Unit tests**: Each module (graph engine, traversal, semantic, merge) tested in isolation with in-memory SQLite
- **Integration tests**: Full MCP tool flow tests (add entities → search → traverse → merge)
- **CLI tests**: Click test runner for all CLI commands
- **Migration tests**: Test each migration applies cleanly on fresh DB and upgrades from previous version
- **Performance tests**: Benchmarks for traversal depth, search latency, batch insert throughput (as reference, not CI-blocking)
- **Edge cases**: Empty graph, single entity, circular relationships, very deep traversal, Unicode entity names, SQL injection attempts

## 16. Future Considerations (not in v1, but designed for)

- **NetworkX integration**: Optional in-memory graph algorithms (centrality, community detection, PageRank) for advanced query planning
- **Graph visualization**: Export to DOT/Mermaid format for visual inspection
- **Multi-graph**: Multiple named graphs per project (e.g., "characters", "locations", "plot")
- **Temporal queries**: Time-scoped queries ("what did we know about X as of last Tuesday?")
- **WebSocket transport**: Real-time graph updates
- **Plugin hooks**: Extensible entity types and relationship validators
