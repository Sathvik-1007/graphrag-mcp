# graphrag-mcp

> Persistent knowledge graph memory for LLM-powered CLI agents

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)

**No API keys. No cloud provider. No external services.** graphrag-mcp is a fully local MCP server that plugs into any MCP-compatible agent (Claude Code, OpenCode, Codex CLI, Gemini CLI, Cursor, Windsurf, Amp) as a standard tool provider. Install it, add it to your MCP config, and your agent immediately gains persistent memory -- nothing else required.

---

## What is this?

LLM-powered coding agents forget everything between sessions. They re-read files, re-discover architecture, and repeat mistakes. **graphrag-mcp** fixes this by giving any MCP-compatible agent a persistent, per-project knowledge graph that combines graph storage, semantic vector search, and multi-hop traversal. It runs entirely locally -- no API provider accounts, no cloud dependencies, no Docker containers. Just `pip install graphrag-mcp` and go.

### Why a graph, not just a vector store?

Vector search finds _similar_ things. Graphs find _connected_ things. When an agent asks "what depends on the auth service?", a vector store returns text that mentions auth. A knowledge graph traverses the actual dependency edges and returns every upstream consumer -- even ones that never mention "auth" in their description. graphrag-mcp gives you both: vector similarity for fuzzy discovery, graph traversal for structural queries.

---

## For your agent's consideration...

Paste this prompt into your agent:

```
I want you to give yourself persistent memory using graphrag-mcp. Run the following:

pip install graphrag-mcp
graphrag-mcp install opencode    # or: claude, codex, gemini, cursor, windsurf, amp

This installs a skill file that teaches you how to use the 14 MCP tools.
The server should already be configured in your MCP config. If not, add it:

{
  "mcpServers": {
    "graphrag-mcp": {
      "command": "graphrag-mcp",
      "args": ["server", "--project-dir", "/path/to/your/project"]
    }
  }
}

Now start using the knowledge graph:

1. read_graph() to see current state
2. search_nodes("relevant topic") to find existing knowledge
3. add_entities, add_relationships, add_observations as you learn things
4. open_dashboard() to explore the graph visually in your browser
5. At session end, capture anything important you discovered

Your goal: build a rich knowledge graph of this project so future sessions
start with full context instead of from zero. Search before adding to avoid
duplicates. Be specific with entity names and types.
```

---

## Installation

### Option 1: pip (Recommended)

```bash
pip install graphrag-mcp
graphrag-mcp server
```

### Option 2: uvx (zero pre-install)

```bash
uvx graphrag-mcp server
```

`uvx` downloads the package into an isolated environment and runs it in one command. Nothing to pre-install beyond [uv](https://docs.astral.sh/uv/).

### Option 3: From source

```bash
git clone https://github.com/Sathvik-1007/graphrag-mcp
cd graphrag-mcp
pip install -e ".[full,dev]"
graphrag-mcp server
```

### Optional extras

```bash
pip install "graphrag-mcp[embeddings]"   # sentence-transformers for local embeddings
pip install "graphrag-mcp[onnx]"         # ONNX runtime for ~3x faster inference
pip install "graphrag-mcp[ui]"           # aiohttp for interactive graph visualisation
pip install "graphrag-mcp[full]"         # all of the above
```

---

## Quick Start

**1. Install the skill for your agent:**

```bash
graphrag-mcp install claude        # Claude Code
graphrag-mcp install opencode      # OpenCode
graphrag-mcp install codex         # Codex CLI
graphrag-mcp install gemini        # Gemini CLI
graphrag-mcp install cursor        # Cursor
graphrag-mcp install windsurf      # Windsurf
graphrag-mcp install amp           # Amp
```

This writes a skill file that teaches your agent how to use all 14 MCP tools -- when to search, when to add entities, naming conventions, and common workflows.

**2. Configure MCP** by adding this to your agent's MCP config:

```json
{
  "mcpServers": {
    "graphrag-mcp": {
      "command": "graphrag-mcp",
      "args": ["server"]
    }
  }
}
```

With full customization:

```json
{
  "mcpServers": {
    "graphrag-mcp": {
      "command": "graphrag-mcp",
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

graphrag-mcp exposes 14 MCP tools -- six for writing, seven for reading, and one utility:

### Write Tools

| Tool | Description |
|------|-------------|
| `add_entities` | Batch-create entities with optional observations |
| `add_relationships` | Create typed, directed edges between entities |
| `add_observations` | Attach factual statements to entities |
| `update_entity` | Modify entity description, properties, or type |
| `delete_entities` | Remove entities with cascade to relationships and observations |
| `merge_entities` | Combine duplicate entities into one |

### Read Tools

| Tool | Description |
|------|-------------|
| `search_nodes` | Hybrid semantic + full-text search with RRF fusion |
| `search_observations` | Semantic search directly over observations |
| `find_connections` | Multi-hop graph traversal between entities |
| `get_entity` | Full entity details with observations and relationships |
| `read_graph` | Graph statistics overview |
| `get_subgraph` | Extract neighborhood around seed entities |
| `find_paths` | Shortest paths between two entities |

### Utility Tools

| Tool | Description |
|------|-------------|
| `open_dashboard` | Launch interactive graph visualisation UI and return its URL |

---

## Architecture

```
Agent (Claude/Codex/Gemini/OpenCode)
  |
  | MCP Protocol (stdio or SSE)
  v
graphrag-mcp server
  |-- Graph Engine ---- entity/relationship/observation CRUD
  |-- Semantic Engine -- sentence-transformers embeddings + hybrid search
  |-- UI Server ------- interactive graph explorer (aiohttp + React SPA)
  '-- Storage --------- pluggable backend (SQLite default, .graphrag/graph.db)
```

Everything lives in a single SQLite database per project. No external services, no Docker containers, no API keys. The server communicates over MCP's standard stdio transport (SSE also supported) and stores all data in `.graphrag/graph.db` at your project root.

The database file is portable -- copy it between machines, check it into version control, or back it up like any other file.

---

## MCP Integration

graphrag-mcp is a standard MCP (Model Context Protocol) server. It does not require any external provider, API key, or cloud account. It communicates with your agent over the MCP protocol (stdio by default, SSE and streamable-http also supported) and exposes 14 tools that the agent can call directly.

**What this means in practice:** once you add graphrag-mcp to your agent's MCP config, the agent sees 14 new tools (`add_entities`, `search_nodes`, `find_connections`, `open_dashboard`, etc.) in its tool list. The agent calls these tools the same way it calls any other MCP tool -- no special SDK, no provider integration, no authentication. It works with every MCP-compatible agent out of the box.

To verify it's working, ask your agent to run `read_graph()` -- it should return the current graph statistics (entity count, relationship count, etc.).

---

## Data Storage

By default, graphrag-mcp stores its database at `.graphrag/graph.db` relative to the current working directory. You can control this with:

| Method | Example | Result |
|--------|---------|--------|
| `--project-dir` | `--project-dir /home/user/myproject` | Stores at `/home/user/myproject/.graphrag/graph.db` |
| `--db` | `--db /custom/path/memory.db` | Stores at exactly that path |
| `GRAPHRAG_DB_PATH` env | `export GRAPHRAG_DB_PATH=/tmp/test.db` | Stores at that path |
| Default | (nothing) | `.graphrag/graph.db` relative to CWD |

**Priority order:** `--db` > `--project-dir` > `GRAPHRAG_DB_PATH` env var > default.

The `.graphrag/` directory is automatically created if it doesn't exist. Add `.graphrag/` to your `.gitignore` if you don't want to track the database in version control.

---

## How It Works

### Entities, Relationships, and Observations

The knowledge graph has three core primitives:

- **Entities** are named nodes with a type and description (e.g., `AuthService`, type `service`).
- **Relationships** are typed, directed edges between entities (e.g., `AuthService --DEPENDS_ON--> Database`).
- **Observations** are factual statements attached to entities (e.g., "Uses bcrypt for password hashing").

### Hybrid Search

`search_nodes` combines three retrieval strategies using Reciprocal Rank Fusion (RRF):

1. **Vector similarity** -- cosine distance against sentence-transformer embeddings of entity names, descriptions, and observations.
2. **Full-text search** -- SQLite FTS5 with BM25 ranking for keyword matching.
3. **RRF fusion** -- merges and re-ranks results from both strategies into a single scored list.

When no embedding model is installed, search gracefully degrades to FTS-only mode.

### Multi-Hop Traversal

`find_connections` walks the graph recursively using SQL CTEs, discovering indirect relationships up to a configurable depth. This surfaces connections that no flat search can find -- like tracing a function through three layers of abstraction to the database schema it ultimately modifies.

### Entity Resolution

When the agent references an entity by name, graphrag-mcp resolves it through a cascade:

1. **Exact match** -- case-sensitive name lookup.
2. **Case-insensitive match** -- normalized comparison.
3. **FTS5 match** -- full-text search for partial or fuzzy names.
4. **Suggestions** -- if nothing matches, return the closest candidates so the agent can self-correct.

---

## CLI Reference

### Server

```bash
graphrag-mcp server                          # stdio transport (default)
graphrag-mcp server --transport sse          # SSE transport
graphrag-mcp server --db /path/to/graph.db   # custom database path
graphrag-mcp server --project-dir /my/project  # store memory in <dir>/.graphrag/

# Embedding customization
graphrag-mcp server --embedding-model sentence-transformers/all-mpnet-base-v2
graphrag-mcp server --no-onnx --embedding-device cuda
graphrag-mcp server --cache-size 50000

# Tuning
graphrag-mcp server --search-limit 20 --max-hops 6
graphrag-mcp server --log-level DEBUG
```

All server options:

| Flag | Description | Default |
|------|-------------|---------|
| `--transport` | `stdio`, `sse`, or `streamable-http` | `stdio` |
| `--db` | Path to SQLite database file | `.graphrag/graph.db` |
| `--project-dir` | Project root; DB at `<dir>/.graphrag/graph.db` | CWD |
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
graphrag-mcp install <agent>                 # project-level install
graphrag-mcp install <agent> --global        # global/user-level install
graphrag-mcp install <agent> --domain code   # use domain overlay (code, research, general)
```

Supported agents: `claude`, `opencode`, `codex`, `gemini`, `cursor`, `windsurf`, `amp`.

### Graph Management

```bash
graphrag-mcp init                            # create .graphrag/ directory
graphrag-mcp init --project-dir /my/project  # create in specific directory
graphrag-mcp status                          # print graph statistics
graphrag-mcp status --json                   # graph statistics as JSON
graphrag-mcp export --format json            # export entire graph
graphrag-mcp export --output backup.json     # export to file
graphrag-mcp import graph.json               # import graph from file
graphrag-mcp validate                        # run integrity checks
```

All management commands accept `--db` and `--project-dir` for targeting a specific database.

### Graph Visualisation UI

```bash
graphrag-mcp ui                              # open interactive graph explorer
graphrag-mcp ui --no-open                    # start server without opening browser
graphrag-mcp ui --port 9090                  # use a specific port
```

The `open_dashboard` MCP tool also starts this UI server and returns the URL directly to your agent -- no browser auto-open, just a link you can visit when ready.

---

## Configuration

All settings are optional. Defaults work out of the box. Every setting can be controlled via CLI flags (see `graphrag-mcp server --help`), environment variables, or both. CLI flags take precedence over environment variables, which take precedence over defaults.

| Environment Variable | CLI Flag | Default | Description |
|---------------------|----------|---------|-------------|
| `GRAPHRAG_DB_PATH` | `--db` | `.graphrag/graph.db` | Database file path |
| `GRAPHRAG_BACKEND_TYPE` | -- | `sqlite` | Storage backend |
| `GRAPHRAG_EMBEDDING_MODEL` | `--embedding-model` | `all-MiniLM-L6-v2` | HuggingFace model ID |
| `GRAPHRAG_USE_ONNX` | `--use-onnx / --no-onnx` | `true` | Use ONNX runtime if available |
| `GRAPHRAG_EMBEDDING_DEVICE` | `--embedding-device` | `cpu` | Inference device (`cpu` or `cuda`) |
| `GRAPHRAG_CACHE_SIZE` | `--cache-size` | `10000` | Embedding cache max entries |
| `GRAPHRAG_SEARCH_LIMIT` | `--search-limit` | `10` | Default search result limit |
| `GRAPHRAG_MAX_HOPS` | `--max-hops` | `4` | Default max traversal depth |
| `GRAPHRAG_LOG_LEVEL` | `--log-level` | `WARNING` | Logging verbosity |
| `GRAPHRAG_TRANSPORT` | `--transport` | `stdio` | MCP transport protocol |

---

## Performance

graphrag-mcp is optimized for low-latency, single-user workloads typical of CLI agent usage:

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
git clone https://github.com/Sathvik-1007/graphrag-mcp
cd graphrag-mcp

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
pytest                            # all tests (323 pass)
pytest tests/test_graph/          # graph engine tests
pytest tests/test_server/         # MCP server tool tests
pytest tests/test_cli/            # CLI command tests
pytest tests/test_models/         # data model tests
pytest tests/test_semantic/       # search + vector tests
pytest tests/test_storage/        # storage backend tests
pytest tests/test_db/             # database + migration tests
pytest tests/test_utils/          # config, logging, ID generation tests
pytest -x -q                      # stop on first failure, quiet output
```

### Project Structure

```
src/graphrag_mcp/
  __init__.py              # package version
  __main__.py              # python -m graphrag_mcp support
  server.py                # MCP server entry point and 14 tool definitions
  cli/
    main.py                # Click CLI: server, init, status, export, import, validate, ui
    install.py             # Skill installer for 7 agent types
  db/
    connection.py          # Database class (aiosqlite, WAL, PRAGMA tuning)
    schema.py              # Migration runner + version tracking
    migrations/            # Versioned SQL migration scripts
  graph/
    engine.py              # GraphEngine -- entity/relationship/observation CRUD
    traversal.py           # GraphTraversal -- BFS, path-finding, subgraph extraction
    merge.py               # EntityMerger -- entity deduplication and merging
  models/
    entity.py              # Entity dataclass
    relationship.py        # Relationship dataclass
    observation.py         # Observation dataclass
  semantic/
    embeddings.py          # EmbeddingEngine -- lazy loading, ONNX, content-hash cache
    search.py              # HybridSearch -- vector + FTS5 + RRF fusion
  storage/
    base.py                # StorageBackend ABC (~37 abstract methods)
    sqlite_backend.py      # SQLiteBackend -- reference implementation
  ui/
    server.py              # aiohttp web server for graph visualisation
    routes.py              # REST API route handlers
    frontend/              # Pre-built React SPA (Sigma.js graph explorer)
  utils/
    config.py              # Environment-variable-based Config dataclass
    errors.py              # 14-class exception hierarchy
    ids.py                 # ULID generation
    logging.py             # Structured logging setup
```

---

## Star History

<a href="https://www.star-history.com/?repos=Sathvik-1007%2Fgraphrag-mcp&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=Sathvik-1007/graphrag-mcp&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=Sathvik-1007/graphrag-mcp&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=Sathvik-1007/graphrag-mcp&type=date&legend=top-left" />
 </picture>
</a>

---

## License

[MIT](LICENSE)
