# Best Practices

## Why Extraction Gets Skipped

The biggest failure mode is not extracting. Here's how the rationalization sounds
and why it's wrong:

| Thought | Reality |
|---------|---------|
| "This turn isn't important enough" | Every turn has extractable information |
| "I'll store it at the end" | You'll forget the details. Store now |
| "This is just a simple answer" | Simple answers contain facts worth persisting |
| "The user didn't ask me to remember" | Extraction is automatic, not user-triggered |
| "I already know this from the graph" | If something was confirmed or changed, record that |
| "There's nothing new here" | Confirmations, clarifications, and corrections are facts |
| "I'll remember without storing" | You won't. Next session starts fresh |

If you catch yourself thinking any of these — that is the signal to extract.

## What to Extract

- **Decisions** and their rationale ("Chose X because Y")
- **Problems** and root causes
- **Architecture** — how systems, components, or concepts connect
- **People** and their roles, responsibilities, opinions
- **Plans** before work begins
- **Implementations** after work completes, including deviations from plan
- **Facts** with dates, numbers, and specifics
- **Corrections** to previously stored information

## What NOT to Extract

- Scratch calculations and temporary exploration
- Transient state that changes every session (e.g., "currently editing file X")
- Raw content dumps — store facts *about* content, not the content itself
- Speculative claims without marking uncertainty (use relationship weight < 1.0)

## Observation Quality

**Atomic**: One fact per observation. This makes facts independently searchable
and independently deletable. "Rate limit changed to 500 AND fix was deployed"
should be two observations.

**Specific**: Include dates, numbers, exact values, names. "Rate limit was
increased from 100 to 500 req/s on 2026-03-15" beats "rate limit changed."

**Complete sentences**: A future agent reading this observation cold should
understand the fact without needing surrounding context.

## Description Freshness

Descriptions summarize what an entity IS right now — not its history. When facts
change, update the description with `update_entity`. A stale description actively
misleads future sessions.

## Relationship Weights

- **1.0** (default): Confirmed, definite
- **0.7–0.9**: High confidence, not definitively confirmed
- **0.4–0.6**: Moderate confidence, needs verification
- **0.1–0.3**: Speculative or tentative

## Choosing the Right Search Tool

| You want to find... | Use |
|---------------------|-----|
| Entities matching a concept | `search_nodes` |
| A specific fact in observation text | `search_observations` |
| Everything about one known entity | `get_entity` |
| What's connected to an entity | `find_connections` |
| How two entities relate | `find_paths` |
| The neighborhood around seed entities | `get_subgraph` |
| Overall graph state | `read_graph` |
| Browse all entities | `list_entities` |

## Granularity

**Too fine**: An entity for every minor detail — every variable, every passing
thought. Store at the level you'd want to recall: systems, decisions, people,
concepts, key findings.

**Too coarse**: One mega-entity with all facts as observations. Break knowledge
into meaningful, searchable units.

**Right level**: One entity per significant concept, decision, person, system,
or milestone. Observations carry the details.

## Anti-Patterns

| Pattern | Why It Hurts | Do Instead |
|---------|-------------|------------|
| Skip extraction ("not important") | Graph becomes empty and useless | Extract every turn |
| Batch writes at session end | You forget 80% of the details | Write during extraction each turn |
| Plans without implementations | Loses outcome context | Always record what happened |
| Empty descriptions | Unsearchable entities | Write meaningful summaries |
| Multiple facts per observation | Can't search or delete individually | One fact = one observation |
| Skip dedup check | Fragments knowledge | Always `search_nodes` first |
| Store raw content dumps | Noise overwhelms signal | Store facts *about* content |
| Never update or delete | Graph goes stale | Maintain actively |
| Vague observations | Worthless in future sessions | Include dates, numbers, specifics |
| Generic entity types | Hard to filter and browse | Use the most specific type that fits |

## Multiple Graphs

graph-mem supports named graphs stored as separate databases in `~/.graphmem/`:

```
create_graph("project-alpha")    → ~/.graphmem/project-alpha.db
switch_graph("project-alpha")    → all tools now use this graph
list_graphs()                    → shows all graphs with stats
delete_graph("old-project")      → removes the database file
```

Use this for separating knowledge by project or domain. The CLI flag
`graph-mem server --graph project-alpha` starts the server on a specific graph.
