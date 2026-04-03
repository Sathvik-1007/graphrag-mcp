# Domain: Research & Academia

When conducting literature reviews, tracking papers, or managing research projects.

## Entity Types

In addition to the core types (`plan`, `implementation`, `decision`, `problem`):

| Type | When to Use |
|------|-------------|
| `paper` | A research paper or publication |
| `author` | A researcher or author |
| `concept` | A theoretical concept, method, or framework |
| `dataset` | A dataset used in research |
| `method` | A specific methodology or algorithm |
| `finding` | A research finding or result |
| `hypothesis` | A hypothesis being tested |
| `venue` | A conference, journal, or publication venue |
| `experiment` | A specific experiment or evaluation |

## Relationship Types

| Type | Direction | Example |
|------|-----------|---------|
| `CITES` | Paper citation | `Paper B` → `Paper A` |
| `AUTHORED_BY` | Authorship | `Paper` → `Author` |
| `USES_METHOD` | Methodology used | `Paper` → `Transformer Architecture` |
| `CONTRADICTS` | Conflicting findings | `Finding B` → `Finding A` |
| `SUPPORTS` | Confirming findings | `Finding B` → `Finding A` |
| `EXTENDS` | Builds on prior work | `Paper B` → `Paper A` |
| `EVALUATED_ON` | Evaluation dataset | `Method` → `GLUE Benchmark` |
| `PUBLISHED_AT` | Publication venue | `Paper` → `NeurIPS 2025` |
| `SUPERSEDES` | Newer work replaces older | `Method v2` → `Method v1` |

## Extraction Heuristics

- Store research plans before starting a literature review or experiment
- Record implementation outcomes (what was found, how it differed from hypothesis)
- Store key findings as observations with exact numbers and claims
- Track citation chains to understand intellectual lineage
- Record methodology details as observations, not just method names
- Link contradictory findings explicitly — these are high-value relationships
- Use `finding` entities for results you want to compare across papers
- Store venue information to track where communities publish
- When a paper makes a strong claim, store it as an observation with the exact quote
- Track which datasets are used by which methods for reproducibility
