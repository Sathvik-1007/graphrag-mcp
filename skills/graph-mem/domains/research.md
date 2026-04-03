# Domain: Research & Academia

When conducting literature reviews, tracking papers, or managing research projects.

## Recommended Entity Types

In addition to the core types (`plan`, `implementation`, `decision`):

- `paper` — A research paper or publication
- `author` — A researcher or author
- `concept` — A theoretical concept, method, or framework
- `dataset` — A dataset used in research
- `method` — A specific methodology or algorithm
- `finding` — A research finding or result
- `hypothesis` — A hypothesis being tested
- `venue` — A conference, journal, or publication venue
- `experiment` — A specific experiment or evaluation

## Recommended Relationship Types

- `CITES` — Paper citation relationships
- `AUTHORED_BY` — Authorship
- `USES_METHOD` — Paper/finding uses a specific method
- `CONTRADICTS` / `SUPPORTS` — Relationship between findings
- `EXTENDS` — Builds upon prior work
- `EVALUATED_ON` — Method evaluated on a dataset
- `PUBLISHED_AT` — Paper published at a venue
- `TARGETS` — Links a plan to the entities it will investigate
- `IMPLEMENTS` — Links an implementation to the plan it fulfils
- `SUPERSEDES` — Newer work that replaces older work

## Heuristics

- Store research plans before starting a literature review or experiment
- Record implementation outcomes (what was found, how it differed from the hypothesis)
- Store key findings as observations on paper entities — quote specific numbers and claims
- Track citation chains to understand intellectual lineage
- Record methodology details as observations, not just method names
- Link contradictory findings explicitly — these are high-value relationships
- Use `finding` entities for results you want to compare across papers
- Store venue information to track where communities publish
- When a paper makes a strong claim, store it as an observation with the exact quote and page
