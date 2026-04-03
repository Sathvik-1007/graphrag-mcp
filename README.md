# graph-mem

> Persistent knowledge graph memory for LLM-powered CLI agents

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)

**No API keys. No cloud provider. No external services.** graph-mem is a fully local MCP server that plugs into any MCP-compatible agent as a standard tool provider. Install it, add it to your MCP config, and your agent immediately gains persistent memory -- nothing else required.

### Supported Agents

<table>
<tr>
<td><b>Claude Code</b></td>
<td><b>OpenCode</b></td>
<td><b>Cursor</b></td>
<td><b>Windsurf</b></td>
<td><b>Codex CLI</b></td>
<td><b>Gemini CLI</b></td>
</tr>
<tr>
<td><b>GitHub Copilot</b></td>
<td><b>Amp</b></td>
<td><b>Kiro</b></td>
<td><b>Roo Code</b></td>
<td><b>Trae</b></td>
<td><b>Augment</b></td>
</tr>
<tr>
<td><b>Continue</b></td>
<td><b>Warp</b></td>
<td><b>KiloCode</b></td>
<td><b>Qoder</b></td>
<td><b>CodeBuddy</b></td>
<td><b>Droid (Factory)</b></td>
</tr>
<tr>
<td colspan="6"><b>Antigravity</b> · and any MCP-compatible agent</td>
</tr>
</table>

---

## What is this?

LLM-powered coding agents forget everything between sessions. They re-read files, re-discover architecture, and repeat mistakes. **graph-mem** fixes this by giving any MCP-compatible agent a persistent, per-project knowledge graph that combines graph storage, semantic vector search, and multi-hop traversal. It runs entirely locally -- no API provider accounts, no cloud dependencies, no Docker containers. Just `pip install graph-mem` and go.

### Why a graph, not just a vector store?

Vector search finds _similar_ things. Graphs find _connected_ things. When an agent asks "what depends on the auth service?", a vector store returns text that mentions auth. A knowledge graph traverses the actual dependency edges and returns every upstream consumer -- even ones that never mention "auth" in their description. graph-mem gives you both: vector similarity for fuzzy discovery, graph traversal for structural queries.

---

## For your agent's consideration...

Paste this prompt into your agent:

```
I want you to give yourself persistent memory using graph-mem. Run the following:

pip install graph-mem
graph-mem install opencode    # or: claude, cursor, windsurf, codex, gemini, copilot, amp, kiro, roocode, trae, augment, continue, warp, kilocode, qoder, codebuddy, droid, antigravity

This installs a skill file that teaches you how to use the 19 MCP tools.
The server should already be configured in your MCP config. If not, add it:

{
  "mcpServers": {
    "graph-mem": {
      "command": "graph-mem",
      "args": ["server", "--project-dir", "/path/to/your/project"]
    }
  }
}

Now start using the knowledge graph:

1. read_graph() to see current state
2. search_nodes("relevant topic") to find existing knowledge
3. add_entities, add_relationships, add_observations as you learn things
4. update_observation / update_relationship to fix mistakes in-place
5. open_dashboard() to explore the graph visually in your browser
6. At session end, capture anything important you discovered

Your goal: build a rich knowledge graph of this project so future sessions
start with full context instead of from zero. Search before adding to avoid
duplicates. Be specific with entity names and types.
```

---

## Installation

### Option 1: pip (Recommended)

```bash
pip install graph-mem
graph-mem server
```

### Option 2: uvx (zero pre-install)

```bash
uvx graph-mem server
```

`uvx` downloads the package into an isolated environment and runs it in one command. Nothing to pre-install beyond [uv](https://docs.astral.sh/uv/).

### Option 3: From source

```bash
git clone https://github.com/Sathvik-1007/GraphMem-MCP
cd graph-mem
pip install -e ".[full,dev]"
graph-mem server
```

### Optional extras

```bash
pip install "graph-mem[embeddings]"   # sentence-transformers for local embeddings
pip install "graph-mem[onnx]"         # ONNX runtime for ~3x faster inference
pip install "graph-mem[ui]"           # aiohttp for interactive graph visualisation
pip install "graph-mem[full]"         # all of the above
```

---

## Quick Start

**1. Install the skill for your agent:**

```bash
graph-mem install claude        # Claude Code
graph-mem install opencode      # OpenCode
graph-mem install cursor        # Cursor
graph-mem install windsurf      # Windsurf
graph-mem install codex         # Codex CLI
graph-mem install gemini        # Gemini CLI
graph-mem install copilot       # GitHub Copilot
graph-mem install amp           # Amp
graph-mem install kiro          # Kiro
graph-mem install roocode       # Roo Code
graph-mem install trae          # Trae
graph-mem install augment       # Augment
graph-mem install continue      # Continue
graph-mem install warp          # Warp
graph-mem install kilocode      # KiloCode
graph-mem install qoder         # Qoder
graph-mem install codebuddy     # CodeBuddy
graph-mem install droid         # Droid (Factory)
graph-mem install antigravity   # Antigravity
```

This writes a skill file that teaches your agent how to use all 19 MCP tools -- when to search, when to add entities, naming conventions, and common workflows.

**2. Configure MCP** by adding this to your agent's MCP config:

```json
{
  "mcpServers": {
    "graph-mem": {
      "command": "graph-mem",
      "args": ["server"]
    }
  }
}
```

With full customization:

```json
{
  "mcpServers": {
    "graph-mem": {
      "command": "graph-mem",
      "args": [
        "server",
        "--project-dir", "/path/to/my/project",
        "--embedding-model", "sentence-transformers/all-mpnet-base-v2",
        "--use-onnx",
        "--cache-size", "20000",
        "--log-level", "INFO"
      ]
    }
  }
}
```

That's it. Your agent now has persistent memory.

---

## Features

graph-mem exposes **19 MCP tools** -- ten for writing, eight for reading, and one utility. Full CRUD on every primitive: entities, relationships, and observations can all be created, read, updated, and deleted.

### Write Tools (10)

| Tool | Description |
|------|-------------|
| `add_entities` | Batch-create entities with optional observations; auto-merges on name conflict |
| `add_relationships` | Create typed, directed edges between entities; merges duplicates by max weight |
| `add_observations` | Attach factual statements to entities with optional source provenance |
| `update_entity` | Modify entity description, properties, or type in-place |
| `update_relationship` | Change weight, type, or properties of an existing edge without delete+re-create |
| `update_observation` | Edit observation text content in-place with automatic embedding recompute |
| `delete_entities` | Remove entities with cascade to relationships, observations, and embeddings |
| `delete_relationships` | Remove specific edges between entities, optionally filtered by type |
| `delete_observations` | Remove specific observations by ID with ownership validation |
| `merge_entities` | Combine duplicate entities: moves observations and relationships, deduplicates edges |

### Read Tools (8)

| Tool | Description |
|------|-------------|
| `search_nodes` | Hybrid semantic + full-text search with RRF fusion ranking |
| `search_observations` | Semantic search directly over observation text content |
| `find_connections` | Multi-hop BFS graph traversal with direction and type filters |
| `get_entity` | Full entity details with all observations and relationships |
| `list_entities` | Browse/paginate all entities with optional type filter |
| `read_graph` | Graph statistics: counts, type distributions, most-connected entities |
| `get_subgraph` | Extract neighborhood subgraph around seed entities |
| `find_paths` | Find shortest paths between two entities via BFS |

### Utility Tools (1)

| Tool | Description |
|------|-------------|
| `open_dashboard` | Launch interactive graph visualisation UI and return its URL |

---

## Architecture

### System Overview

```mermaid
graph TB
    subgraph Agents["Any MCP-Compatible Agent"]
        A1["Claude Code"]
        A2["OpenCode"]
        A3["Cursor"]
        A4["Gemini CLI"]
        A5["19 others..."]
    end

    subgraph Transport["MCP Transport Layer"]
        STDIO["stdio<br/>(default)"]
        SSE["SSE"]
        HTTP["streamable-http"]
    end

    subgraph Server["graph-mem Server"]
        direction TB
        subgraph WriteTools["Write Tools (10)"]
            WT1["add_entities"]
            WT2["add_relationships"]
            WT3["add_observations"]
            WT4["update_entity"]
            WT5["update_relationship"]
            WT6["update_observation"]
            WT7["delete_entities"]
            WT8["delete_relationships"]
            WT9["delete_observations"]
            WT10["merge_entities"]
        end
        subgraph ReadTools["Read Tools (8)"]
            RT1["search_nodes"]
            RT2["search_observations"]
            RT3["find_connections"]
            RT4["get_entity"]
            RT5["list_entities"]
            RT6["read_graph"]
            RT7["get_subgraph"]
            RT8["find_paths"]
        end
        subgraph Utility["Utility (1)"]
            UT1["open_dashboard"]
        end
    end

    subgraph Engines["Core Engines"]
        GE["GraphEngine<br/>CRUD + resolution"]
        SE["HybridSearch<br/>vector + FTS5 + RRF"]
        EE["EmbeddingEngine<br/>sentence-transformers"]
        GT["GraphTraversal<br/>BFS + pathfinding"]
        EM["EntityMerger<br/>dedup + consolidate"]
    end

    subgraph Storage["SQLite Storage Layer"]
        DB["SQLite WAL<br/>.graphmem/graph.db"]
        VEC["sqlite-vec<br/>vector index"]
        FTS["FTS5<br/>full-text index"]
        MIG["Versioned migrations"]
    end

    subgraph Dashboard["Interactive Dashboard"]
        AIOHTTP["aiohttp server"]
        REACT["React SPA<br/>canvas graph explorer"]
    end

    Agents --> Transport
    Transport --> Server
    WriteTools --> GE
    WriteTools --> EE
    ReadTools --> SE
    ReadTools --> GT
    ReadTools --> GE
    UT1 --> Dashboard
    GE --> DB
    SE --> VEC
    SE --> FTS
    GT --> DB
    EM --> DB
    EE --> VEC
    AIOHTTP --> DB

    style Agents fill:#6366f1,stroke:#4f46e5,color:#fff
    style Server fill:#0ea5e9,stroke:#0284c7,color:#fff
    style Storage fill:#f59e0b,stroke:#d97706,color:#fff
    style Engines fill:#8b5cf6,stroke:#7c3aed,color:#fff
    style Dashboard fill:#10b981,stroke:#059669,color:#fff
```

Everything lives in a single SQLite database per project. No external services, no Docker containers, no API keys. The server communicates over MCP's standard stdio transport (SSE also supported) and stores all data in `.graphmem/graph.db` at your project root.

The database file is portable -- copy it between machines, check it into version control, or back it up like any other file.

---

### Tool Request Flow

Every tool call follows the same pattern through the stack:

```mermaid
sequenceDiagram
    participant Agent as LLM Agent
    participant MCP as MCP Protocol
    participant Tool as Tool Function
    participant Engine as GraphEngine
    participant Embed as EmbeddingEngine
    participant Storage as SQLiteBackend
    participant DB as SQLite DB

    Agent->>MCP: tool call (e.g. add_entities)
    MCP->>Tool: dispatch to handler
    Tool->>Engine: validate + build domain objects
    Engine->>Storage: begin transaction
    Storage->>DB: INSERT/UPDATE/DELETE
    DB-->>Storage: result
    Storage-->>Engine: commit
    Engine-->>Tool: domain result
    Tool->>Embed: compute embeddings (async)
    Embed->>Storage: upsert vectors
    Tool-->>MCP: JSON response
    MCP-->>Agent: tool result
```

---

## MCP Integration

graph-mem is a standard MCP (Model Context Protocol) server. It does not require any external provider, API key, or cloud account. It communicates with your agent over the MCP protocol (stdio by default, SSE and streamable-http also supported) and exposes 19 tools that the agent can call directly.

**What this means in practice:** once you add graph-mem to your agent's MCP config, the agent sees 19 new tools (`add_entities`, `search_nodes`, `find_connections`, `update_observation`, `open_dashboard`, etc.) in its tool list. The agent calls these tools the same way it calls any other MCP tool -- no special SDK, no provider integration, no authentication. It works with every MCP-compatible agent out of the box.

To verify it's working, ask your agent to run `read_graph()` -- it should return the current graph statistics (entity count, relationship count, etc.).

---

## Data Storage

By default, graph-mem stores its database at `.graphmem/graph.db` relative to the current working directory. You can control this with:

| Method | Example | Result |
|--------|---------|--------|
| `--project-dir` | `--project-dir /home/user/myproject` | Stores at `/home/user/myproject/.graphmem/graph.db` |
| `--db` | `--db /custom/path/memory.db` | Stores at exactly that path |
| `GRAPHMEM_DB_PATH` env | `export GRAPHMEM_DB_PATH=/tmp/test.db` | Stores at that path |
| Default | (nothing) | `.graphmem/graph.db` relative to CWD |

**Priority order:** `--db` > `--project-dir` > `GRAPHMEM_DB_PATH` env var > default.

The `.graphmem/` directory is automatically created if it doesn't exist. Add `.graphmem/` to your `.gitignore` if you don't want to track the database in version control.

---

## How It Works

### Data Model

The knowledge graph has three core primitives. Every primitive supports full CRUD -- create, read, update, and delete:

```mermaid
erDiagram
    ENTITY {
        string id PK "ULID primary key"
        string name UK "unique display name"
        string entity_type "person, service, concept, etc."
        string description "rich text description"
        json properties "arbitrary key-value metadata"
        float created_at "unix timestamp"
        float updated_at "unix timestamp"
    }
    OBSERVATION {
        string id PK "ULID primary key"
        string entity_id FK "parent entity"
        string content "atomic factual statement"
        string source "provenance (session, doc, etc.)"
        float created_at "unix timestamp"
    }
    RELATIONSHIP {
        string id PK "ULID primary key"
        string source_id FK "source entity"
        string target_id FK "target entity"
        string relationship_type "depends_on, uses, etc."
        float weight "0.0 to 1.0 strength"
        json properties "arbitrary edge metadata"
        float created_at "unix timestamp"
        float updated_at "unix timestamp"
    }
    ENTITY_EMBEDDING {
        string id FK "entity_id"
        blob embedding "float32 vector"
    }
    OBSERVATION_EMBEDDING {
        string id FK "observation_id"
        blob embedding "float32 vector"
    }

    ENTITY ||--o{ OBSERVATION : "has observations"
    ENTITY ||--o{ RELATIONSHIP : "source of"
    ENTITY ||--o{ RELATIONSHIP : "target of"
    ENTITY ||--o| ENTITY_EMBEDDING : "vector index"
    OBSERVATION ||--o| OBSERVATION_EMBEDDING : "vector index"
```

- **Entities** are named nodes with a type and description (e.g., `AuthService`, type `service`).
- **Relationships** are typed, directed, weighted edges between entities (e.g., `AuthService --DEPENDS_ON--> Database`).
- **Observations** are factual statements attached to entities (e.g., "Uses bcrypt for password hashing").
- **Embeddings** are sentence-transformer vectors stored alongside entities and observations for semantic search.

### CRUD Operations Map

```mermaid
graph LR
    subgraph Entities["Entity CRUD"]
        E_C["add_entities<br/>create + auto-merge"]
        E_R["get_entity<br/>list_entities"]
        E_U["update_entity<br/>description, type, props"]
        E_D["delete_entities<br/>cascade to obs + rels"]
        E_M["merge_entities<br/>consolidate duplicates"]
    end

    subgraph Relationships["Relationship CRUD"]
        R_C["add_relationships<br/>create + dedup"]
        R_R["find_connections<br/>get_subgraph<br/>find_paths"]
        R_U["update_relationship<br/>weight, type, props"]
        R_D["delete_relationships<br/>by source+target+type"]
    end

    subgraph Observations["Observation CRUD"]
        O_C["add_observations<br/>attach to entity"]
        O_R["search_observations<br/>get_entity (includes obs)"]
        O_U["update_observation<br/>edit content in-place"]
        O_D["delete_observations<br/>by ID with validation"]
    end

    style Entities fill:#6366f1,stroke:#4f46e5,color:#fff
    style Relationships fill:#0ea5e9,stroke:#0284c7,color:#fff
    style Observations fill:#10b981,stroke:#059669,color:#fff
```

### Hybrid Search Pipeline

`search_nodes` combines three retrieval strategies using Reciprocal Rank Fusion (RRF):

```mermaid
graph TB
    Query["Search Query<br/>'authentication service'"]

    subgraph VectorPath["Vector Search Path"]
        Encode["Encode query<br/>sentence-transformers"]
        VecSearch["sqlite-vec cosine search<br/>top-K nearest neighbors"]
        VecRank["Vector rankings<br/>(entity_id, distance)"]
    end

    subgraph FTSPath["Full-Text Search Path"]
        Tokenize["Tokenize + stem query<br/>FTS5 query syntax"]
        FTSSearch["SQLite FTS5 BM25 search<br/>entities + observations"]
        FTSRank["FTS rankings<br/>(entity_id, bm25_score)"]
    end

    subgraph Fusion["RRF Fusion"]
        Merge["Reciprocal Rank Fusion<br/>score = sum(1 / (k + rank_i))"]
        Dedup["Deduplicate + merge scores"]
        Sort["Sort by fused score"]
    end

    subgraph Enrich["Result Enrichment"]
        FetchEntity["Fetch entity details"]
        FetchRels["Fetch relationships"]
        FetchObs["Fetch observations<br/>(if include_observations=true)"]
    end

    Results["Final scored results<br/>entities with relationships + observations"]

    Query --> VectorPath
    Query --> FTSPath
    VecRank --> Fusion
    FTSRank --> Fusion
    Sort --> Enrich
    Enrich --> Results

    style Query fill:#6366f1,stroke:#4f46e5,color:#fff
    style Fusion fill:#f59e0b,stroke:#d97706,color:#fff
    style Results fill:#10b981,stroke:#059669,color:#fff
```

1. **Vector similarity** -- cosine distance against sentence-transformer embeddings of entity names, descriptions, and observations.
2. **Full-text search** -- SQLite FTS5 with BM25 ranking for keyword matching.
3. **RRF fusion** -- merges and re-ranks results from both strategies into a single scored list.

When no embedding model is installed, search gracefully degrades to FTS-only mode.

### Multi-Hop Traversal

`find_connections` walks the graph recursively using SQL CTEs, discovering indirect relationships up to a configurable depth. This surfaces connections that no flat search can find -- like tracing a function through three layers of abstraction to the database schema it ultimately modifies.

```mermaid
graph LR
    A["AuthService"] -->|DEPENDS_ON| B["UserStore"]
    B -->|READS_FROM| C["PostgresDB"]
    C -->|HOSTS| D["users_table"]

    style A fill:#f472b6,stroke:#ec4899,color:#fff
    style D fill:#34d399,stroke:#10b981,color:#fff
```

A query like `find_connections("AuthService", max_hops=3)` traverses the full chain `AuthService -> UserStore -> PostgresDB -> users_table`, even though `users_table` never mentions "auth."

### Entity Resolution

When the agent references an entity by name, graph-mem resolves it through a cascade:

```mermaid
flowchart TD
    Input["Agent references entity name<br/>(e.g. 'authservice')"]
    Exact["1. Exact match<br/>name = 'authservice'<br/>+ optional type constraint"]
    CI["2. Case-insensitive match<br/>LOWER(name) = 'authservice'"]
    FTS["3. FTS5 fuzzy search<br/>similar names via full-text index"]
    Found["Entity resolved<br/>return Entity object with ID"]
    Suggest["Entity not found<br/>return top-5 suggestions<br/>so agent can self-correct"]

    Input --> Exact
    Exact -->|"found"| Found
    Exact -->|"miss"| CI
    CI -->|"found"| Found
    CI -->|"miss"| FTS
    FTS -->|"found"| Found
    FTS -->|"miss"| Suggest

    style Found fill:#10b981,stroke:#059669,color:#fff
    style Suggest fill:#f59e0b,stroke:#d97706,color:#fff
    style Input fill:#6366f1,stroke:#4f46e5,color:#fff
```

1. **Exact match** -- case-sensitive name lookup, optionally scoped by entity type.
2. **Case-insensitive match** -- normalized comparison.
3. **FTS5 match** -- full-text search for partial or fuzzy names.
4. **Suggestions** -- if nothing matches, return the closest candidates so the agent can self-correct.

### Storage Backend Architecture

```mermaid
graph TB
    subgraph ABC["StorageBackend ABC (50+ abstract methods)"]
        direction LR
        Life["Lifecycle<br/>initialize · close · transaction"]
        EntOps["Entity Ops<br/>upsert · get · list · update · delete · count"]
        RelOps["Relationship Ops<br/>upsert · get · update · delete · count"]
        ObsOps["Observation Ops<br/>insert · get · update · delete · move · count"]
        EmbOps["Embedding Ops<br/>upsert · delete · vector_search · cache"]
        FTSOps["FTS Ops<br/>search_entities · search_observations · suggest"]
        Meta["Metadata + Traversal<br/>get/set metadata · fetch_all · fetch_one"]
    end

    subgraph SQLite["SQLiteBackend (reference implementation)"]
        WAL["WAL mode<br/>concurrent reads"]
        VEC2["sqlite-vec<br/>ANN vectors"]
        FTS2["FTS5 + triggers<br/>auto-sync index"]
        PRAGMA["PRAGMA tuning<br/>journal, cache, mmap"]
    end

    subgraph Future["Future Backends"]
        Neo4j["Neo4j"]
        Memgraph["Memgraph"]
        PG["PostgreSQL"]
    end

    ABC --> SQLite
    ABC -.-> Future

    style ABC fill:#6366f1,stroke:#4f46e5,color:#fff
    style SQLite fill:#0ea5e9,stroke:#0284c7,color:#fff
    style Future fill:#94a3b8,stroke:#64748b,color:#fff
```

---

## CLI Reference

### Server

```bash
graph-mem server                          # stdio transport (default)
graph-mem server --transport sse          # SSE transport
graph-mem server --db /path/to/graph.db   # custom database path
graph-mem server --project-dir /my/project  # store memory in <dir>/.graphmem/

# Embedding customization
graph-mem server --embedding-model sentence-transformers/all-mpnet-base-v2
graph-mem server --no-onnx --embedding-device cuda
graph-mem server --cache-size 50000

# Tuning
graph-mem server --search-limit 20 --max-hops 6
graph-mem server --log-level DEBUG
```

All server options:

| Flag | Description | Default |
|------|-------------|---------|
| `--transport` | `stdio`, `sse`, or `streamable-http` | `stdio` |
| `--db` | Path to SQLite database file | `.graphmem/graph.db` |
| `--project-dir` | Project root; DB at `<dir>/.graphmem/graph.db` | CWD |
| `--host` | Bind address (SSE/HTTP only) | `127.0.0.1` |
| `--port` | Port (SSE/HTTP only) | `8080` |
| `--embedding-model` | HuggingFace model ID for embeddings | `all-MiniLM-L6-v2` |
| `--use-onnx / --no-onnx` | Force ONNX runtime on/off | auto-detect |
| `--embedding-device` | `cpu` or `cuda` | `cpu` |
| `--cache-size` | Embedding LRU cache max entries | `10000` |
| `--search-limit` | Default max results for `search_nodes` | `10` |
| `--max-hops` | Default max depth for `find_connections` | `4` |
| `--log-level` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` | `WARNING` |

### Skill Installation

```bash
graph-mem install <agent>                 # project-level install
graph-mem install <agent> --global        # global/user-level install
graph-mem install <agent> --domain code   # use domain overlay (code, research, general)
```

Supported agents: `claude`, `opencode`, `cursor`, `windsurf`, `codex`, `gemini`, `copilot`, `amp`, `kiro`, `roocode`, `trae`, `augment`, `continue`, `warp`, `kilocode`, `qoder`, `codebuddy`, `droid`, `antigravity`.

### Graph Management

```bash
graph-mem init                            # create .graphmem/ directory
graph-mem init --project-dir /my/project  # create in specific directory
graph-mem status                          # print graph statistics
graph-mem status --json                   # graph statistics as JSON
graph-mem export --format json            # export entire graph
graph-mem export --output backup.json     # export to file
graph-mem import graph.json               # import graph from file
graph-mem validate                        # run integrity checks
```

All management commands accept `--db` and `--project-dir` for targeting a specific database.

### Graph Visualisation UI

```bash
graph-mem ui                              # open interactive graph explorer
graph-mem ui --no-open                    # start server without opening browser
graph-mem ui --port 9090                  # use a specific port
```

The `open_dashboard` MCP tool also starts this UI server and returns the URL directly to your agent -- no browser auto-open, just a link you can visit when ready.

---

## Configuration

All settings are optional. Defaults work out of the box. Every setting can be controlled via CLI flags (see `graph-mem server --help`), environment variables, or both. CLI flags take precedence over environment variables, which take precedence over defaults.

| Environment Variable | CLI Flag | Default | Description |
|---------------------|----------|---------|-------------|
| `GRAPHMEM_DB_PATH` | `--db` | `.graphmem/graph.db` | Database file path |
| `GRAPHMEM_BACKEND_TYPE` | -- | `sqlite` | Storage backend |
| `GRAPHMEM_EMBEDDING_MODEL` | `--embedding-model` | `all-MiniLM-L6-v2` | HuggingFace model ID |
| `GRAPHMEM_USE_ONNX` | `--use-onnx / --no-onnx` | `true` | Use ONNX runtime if available |
| `GRAPHMEM_EMBEDDING_DEVICE` | `--embedding-device` | `cpu` | Inference device (`cpu` or `cuda`) |
| `GRAPHMEM_CACHE_SIZE` | `--cache-size` | `10000` | Embedding cache max entries |
| `GRAPHMEM_SEARCH_LIMIT` | `--search-limit` | `10` | Default search result limit |
| `GRAPHMEM_MAX_HOPS` | `--max-hops` | `4` | Default max traversal depth |
| `GRAPHMEM_LOG_LEVEL` | `--log-level` | `WARNING` | Logging verbosity |
| `GRAPHMEM_TRANSPORT` | `--transport` | `stdio` | MCP transport protocol |

---

## Performance

graph-mem is optimized for low-latency, single-user workloads typical of CLI agent usage:

- **WAL mode + PRAGMA tuning** -- concurrent reads with fast writes, optimized journal and cache settings.
- **ONNX-optimized embeddings** -- ~3x faster inference than default PyTorch, with automatic fallback.
- **Content-hash embedding cache** -- identical text is never embedded twice.
- **Background model pre-warming** -- the embedding model loads in a background thread during server startup, so the first search responds fast without blocking or timing out.
- **Thread-safe lazy loading** -- embedding model initialization uses double-check locking for safe concurrent access.
- **Memory-mapped I/O** -- large databases stay fast without consuming proportional RAM.
- **Batch transactions** -- bulk operations (e.g., `add_entities` with 50 items) execute in a single transaction.

---

## Development

### Setup

```bash
git clone https://github.com/Sathvik-1007/GraphMem-MCP
cd graph-mem

# Using uv (recommended)
uv venv
uv pip install -e ".[full,dev]"

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[full,dev]"
```

### Running Tests

```bash
pytest                            # all tests (340 pass)
pytest tests/test_graph/          # graph engine tests
pytest tests/test_server/         # MCP server tool tests (all 19 tools)
pytest tests/test_cli/            # CLI command tests
pytest tests/test_models/         # data model tests
pytest tests/test_semantic/       # search + vector tests
pytest tests/test_storage/        # storage backend tests
pytest tests/test_db/             # database + migration tests
pytest tests/test_utils/          # config, logging, ID generation tests
pytest -x -q                      # stop on first failure, quiet output
```

### Project Structure

```mermaid
graph TD
    Root["src/graph_mem/"]

    Entry["server.py<br/>MCP entry point<br/>19 tool definitions<br/>lifespan + embedding helpers"]
    CLI["cli/<br/>main.py -- Click CLI commands<br/>install.py -- 19-agent skill installer"]
    DB["db/<br/>connection.py -- aiosqlite wrapper<br/>schema.py -- migration runner<br/>migrations/ -- versioned SQL"]
    GraphMod["graph/<br/>engine.py -- CRUD + entity resolution<br/>traversal.py -- BFS + pathfinding + subgraph<br/>merge.py -- entity consolidation"]
    Models["models/<br/>entity.py -- Entity dataclass<br/>relationship.py -- Relationship dataclass<br/>observation.py -- Observation dataclass"]
    SemanticMod["semantic/<br/>embeddings.py -- lazy model + ONNX + cache<br/>search.py -- hybrid vector+FTS5+RRF"]
    StorageMod["storage/<br/>base.py -- StorageBackend ABC (50+ methods)<br/>sqlite_backend.py -- reference impl<br/>__init__.py -- backend registry"]
    UIMod["ui/<br/>server.py -- aiohttp app factory<br/>routes.py -- REST API endpoints<br/>frontend/ -- pre-built React SPA"]
    Utils["utils/<br/>config.py -- Config dataclass + env vars<br/>errors.py -- 14 error classes<br/>ids.py -- ULID generation<br/>logging.py -- structured logging"]

    Root --> Entry
    Root --> CLI
    Root --> DB
    Root --> GraphMod
    Root --> Models
    Root --> SemanticMod
    Root --> StorageMod
    Root --> UIMod
    Root --> Utils

    style Root fill:#6366f1,stroke:#4f46e5,color:#fff
    style Entry fill:#0ea5e9,stroke:#0284c7,color:#fff
```

| Module | Responsibility |
|--------|---------------|
| `server.py` | MCP server entry point, registers all 19 tools, lifespan management, embedding orchestration |
| `cli/` | Click CLI commands (server, init, status, export, import, validate, ui) + skill installer for 19 agents |
| `db/` | Database class (aiosqlite, WAL mode, PRAGMA tuning) + versioned migrations |
| `graph/` | GraphEngine CRUD, BFS traversal, path-finding, subgraph extraction, entity merging |
| `models/` | Dataclasses for Entity, Relationship, Observation |
| `semantic/` | EmbeddingEngine (lazy loading, ONNX, content-hash cache) + HybridSearch (vector + FTS5 + RRF) |
| `storage/` | StorageBackend ABC (50+ methods) + SQLiteBackend reference implementation + backend registry |
| `ui/` | aiohttp web server + REST API routes + pre-built React SPA graph explorer |
| `utils/` | Config, structured logging, error hierarchy (14 classes), ULID generation |

---

## Star History

<a href="https://www.star-history.com/?repos=Sathvik-1007%2FGraphMem-MCP&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=Sathvik-1007/GraphMem-MCP&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=Sathvik-1007/GraphMem-MCP&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=Sathvik-1007/GraphMem-MCP&type=date&legend=top-left" />
 </picture>
</a>

---

## License

[MIT](LICENSE)
