# Domain: Research & Academia

## Recommended Entity Types

- `paper` — A research paper or publication
- `author` — A researcher or author
- `concept` — A theoretical concept, method, or framework
- `dataset` — A dataset used in research
- `method` — A specific methodology or algorithm
- `finding` — A research finding or result
- `hypothesis` — A hypothesis being tested

## Recommended Relationship Types

- `CITES` — Paper citation relationships
- `AUTHORED_BY` — Authorship
- `USES_METHOD` — Paper/finding uses a specific method
- `CONTRADICTS` / `SUPPORTS` — Relationship between findings
- `EXTENDS` — Builds upon prior work
- `EVALUATED_ON` — Method evaluated on a dataset

## Heuristics

- Store key findings as observations on paper entities
- Track citation chains to understand intellectual lineage
- Record methodology details as observations, not just method names
- Link contradictory findings explicitly — these are high-value relationships
