# Best Practices

## The Ouroboros Pattern

The graph should document the work, and the work should maintain the graph. This
self-referential pattern means:

- Store key concepts, entities, and relationships as you discover them
- Record decisions with rationale as observations
- Track which domain you're working in and what matters most
- Update the graph when understanding evolves
- **Store plans before work begins and implementations after work ends**

The graph eats its own tail: it documents the work, and the work maintains the graph.

### Plan → Implementation → Future Plan

Every significant task should create two linked entities:

1. **Plan entity** (type: `plan`) — Created *before* work begins
   - Captures intent, constraints, acceptance criteria
   - Observations track planned steps and goals
   - Related to the entities it will affect

2. **Implementation entity** (type: `implementation`) — Created *after* work completes
   - Captures what was actually done, including deviations
   - Observations track outcomes, metrics, lessons learned
   - Linked to the plan via `IMPLEMENTS` relationship

Future sessions search for these to understand both *why* something was done (plan)
and *how* it was done (implementation). This trail of intent and execution is what
makes the graph genuinely useful across long-running projects.

## Memory Hygiene

- **Atomic observations**: One fact per observation. Splitting facts makes them independently searchable.
- **Description freshness**: Entity descriptions should summarize current state. Update after significant changes.
- **Relationship weights**: Use 0.0-1.0 to indicate confidence. Default 1.0 for definite relationships, lower for uncertain ones.
- **Search before storing**: Always check if an entity exists before creating a new one. Duplicates fragment your knowledge.
- **Regular pruning**: Periodically `read_graph` and review. Delete entities that are no longer relevant.

## Granularity Guidelines

**Too granular**: Don't create entities for every minor detail. Store things at the level
you'd want to recall them — systems, decisions, people, concepts, key findings.

**Too coarse**: Don't create one entity per project with all facts as observations.
Break knowledge into meaningful, searchable units.

**Right level**: One entity per significant concept, decision, person, system, or
milestone. Observations capture the details — dates, metrics, rationale, quotes.

## Anti-Patterns

**Stale descriptions**: An entity description that no longer reflects reality is worse
than no description. Update or delete stale entities.

**Search without reading**: `search_nodes` returns summaries. Always follow up with
`get_entity` to see the full picture including observations before making decisions.

**Storing raw content**: Observations should be facts *about* content, not the content itself.
"The paper introduces a novel attention mechanism that reduces quadratic complexity to linear"
is useful. Pasting the entire abstract is not.

**Write-once mentality**: The graph is not an append-only log. Update descriptions,
merge duplicates, delete stale entities. A maintained graph is worth 10x an abandoned one.

**Session-end-only writes**: Don't batch all your graph updates to the end of a session.
You'll forget details and skip most of them. Write as you go.

**Plans without implementations**: Storing a plan but never recording the implementation
means you lose the most valuable context — what actually happened and why it deviated.

**Implementations without plans**: Recording what you did without documenting the original
intent makes it impossible to understand design decisions in future sessions.

## When NOT to Store

- Transient working context (scratch calculations, temporary exploration)
- Information that changes every session (current file being edited, current tab open)
- Things better handled by other tools (code diffs in version control, chat logs)
- Speculative or uncertain information without marking it as such
