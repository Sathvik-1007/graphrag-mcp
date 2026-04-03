# Best Practices

## The Extraction Imperative

The knowledge graph is only as good as what you put into it. The single biggest failure
mode is skipping extraction — either entirely or partially. This section exists to make
that failure mode impossible.

### Red Flags — Stop and Extract

If you catch yourself thinking any of these, you MUST stop and run the extraction pass:

| Thought | Reality |
|---------|---------|
| "This turn isn't important enough" | Every turn has extractable information. |
| "I'll store it at the end of the session" | You'll forget details. Store now. |
| "This is just a simple answer" | Simple answers contain facts worth persisting. |
| "The user didn't ask me to remember this" | Extraction is automatic, not user-triggered. |
| "I already know this from the graph" | If something changed or was confirmed, record that. |
| "There's nothing new here" | Confirmations, clarifications, and corrections are all facts. |
| "I'll remember this without storing it" | You won't. Next session starts fresh. |

### What to Extract (Non-Exhaustive)

- **Decisions** and their rationale ("Chose X because Y")
- **Problems** and their root causes
- **Architecture** discoveries (how systems connect)
- **People** and their roles, responsibilities, opinions
- **Plans** before work begins
- **Implementations** after work completes, including deviations
- **Facts** with dates, numbers, and specific details
- **Corrections** to previously stored information
- **Relationships** between any of the above

### What NOT to Extract

- Transient working context (scratch calculations, temporary exploration)
- Information that changes every session (current file being edited)
- Raw content dumps (store facts *about* content, not the content itself)
- Speculative information without marking it as uncertain (use weight < 1.0)
- Things better handled by version control (exact code diffs)

## The Socratic Self-Check Protocol

After every extraction pass, run this interrogation:

### 1. Completeness Check

"Did I capture every entity mentioned or implied in this turn?"

Scan for: proper nouns, system names, technical terms, role references, document
names, tool names, API endpoints, error messages, and concepts introduced.

### 2. Type Accuracy Check

"Did I assign the most specific and accurate entity type?"

Common mis-types:
- `concept` when `method` or `pattern` is more accurate
- `system` when `module` or `api` is more specific
- `person` when `organization` or `team` is what was meant
- `document` when `paper`, `config`, or `artifact` fits better

### 3. Relationship Completeness Check

"Are there implicit relationships I didn't capture?"

Look for:
- Co-occurrence (two entities discussed in the same sentence → likely related)
- Causal language ("because", "due to", "as a result" → `CAUSED_BY`)
- Dependency language ("needs", "requires", "uses" → `DEPENDS_ON`)
- Hierarchy language ("part of", "within", "belongs to" → `PART_OF`)

### 4. Reasoning Preservation Check

"Did I store conclusions without their reasoning?"

If you stored "Decision: Use PostgreSQL" but not *why*, add an observation:
"Chose PostgreSQL over MongoDB because the billing system requires ACID transactions"

### 5. Future Utility Check

"Could a fresh agent reconstruct the context from what I stored?"

Imagine a new session with zero memory except the graph. Would the stored entities,
observations, and relationships be enough to understand what happened and why?

## Memory Hygiene

### Atomic Observations

One fact per observation. This makes facts independently searchable and deletable.

Bad: "Rate limit was changed to 500 req/s and the deployment was rolled out to prod"
Good: Two observations — "Rate limit increased to 500 req/s on 2026-03-15" and
"Rate limit change deployed to production on 2026-03-15"

### Description Freshness

Entity descriptions summarize the current state. When facts change, update the
description. A stale description is worse than no description — it actively misleads.

### Relationship Weights

- `1.0` (default): Definite, confirmed relationship
- `0.7–0.9`: High confidence but not definitively confirmed
- `0.4–0.6`: Moderate confidence, needs verification
- `0.1–0.3`: Speculative or tentative

### Search Before Store

ALWAYS `search_nodes` before `add_entities`. Duplicates fragment knowledge and degrade
search quality. This is the single most important hygiene rule.

### Active Maintenance

The graph is not an append-only log. Update descriptions when facts change. Merge
duplicates when found. Delete entities that are no longer relevant. A maintained graph
is worth 10x an abandoned one.

## Granularity Guidelines

**Too granular**: Creating entities for every variable name, every minor function,
every passing thought. Store at the level you'd want to recall — systems, decisions,
people, concepts, key findings.

**Too coarse**: One entity per project with all facts as observations. Break knowledge
into meaningful, searchable units.

**Right level**: One entity per significant concept, decision, person, system, or
milestone. Observations capture the details.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skip extraction ("not important") | Graph becomes empty and useless | Extract every turn, no exceptions |
| Batch writes at session end | You'll forget 80% of the details | Write during Pass 2 of each turn |
| Plans without implementations | Loses outcome context | Always record what happened |
| Empty descriptions | Unsearchable entities | Write meaningful summaries |
| Multiple facts per observation | Can't search or delete individually | One fact = one observation |
| Skip dedup check | Fragments knowledge | Always search_nodes first |
| Store raw content dumps | Noise overwhelms signal | Store facts *about* content |
| Never update or delete | Graph becomes stale | Maintain actively |
| Vague observations | Worthless in future sessions | Include dates, numbers, specifics |
| Generic entity types | Hard to filter and browse | Use the most specific type |

## Multi-Graph Usage

graph-mem supports multiple named graphs stored as separate `.db` files in `~/.graphmem/`.
Use this for different knowledge domains or projects:

```
create_graph("project-alpha")    → ~/.graphmem/project-alpha.db
switch_graph("project-alpha")    → all tools now use this graph
list_graphs()                    → shows all graphs with counts
delete_graph("old-project")      → removes the graph file
```

CLI flag: `graph-mem server --graph project-alpha`
