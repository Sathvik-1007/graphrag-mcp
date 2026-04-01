# Best Practices

## Memory Hygiene

- **Atomic observations**: One fact per observation. Splitting facts makes them independently searchable.
- **Description freshness**: Entity descriptions should summarize current state. Update after significant changes.
- **Relationship weights**: Use 0.0-1.0 to indicate confidence. Default 1.0 for definite relationships, lower for uncertain ones.
- **Search before storing**: Always check if an entity exists before creating a new one. Duplicates fragment your knowledge.
- **Regular pruning**: Periodically `read_graph` and review. Delete entities that are no longer relevant.

## Anti-Patterns

**Too granular**: Don't create entities for every variable, function parameter, or config key.
Store things at the level you'd want to recall them — services, decisions, people, concepts.

**Too coarse**: Don't create one entity per project with all facts as observations.
Break knowledge into meaningful, searchable units.

**Stale descriptions**: An entity description that says "handles auth" when the service was
rewritten to handle billing is worse than no description. Update or delete stale entities.

**Search without reading**: `search_nodes` returns summaries. Always follow up with
`get_entity` to see the full picture including observations before making decisions.

**Storing file contents**: Observations should be facts about code, not the code itself.
"AuthService uses bcrypt for password hashing" is useful. Pasting the entire file is not.

## When NOT to Store

- Transient debugging information (stack traces, temporary test data)
- Information that changes every session (current file being edited)
- Things better handled by version control (code history, diffs)
- Personal preferences or ephemeral context (your current mood about the codebase)
