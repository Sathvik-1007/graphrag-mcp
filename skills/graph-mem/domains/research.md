# Domain: Research & Academia

For literature reviews, paper tracking, research projects, and academic work.

## Entity Types

Beyond the core types (`plan`, `implementation`, `decision`, `problem`):

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
| `SUPERSEDES` | Newer replaces older | `Method v2` → `Method v1` |

## Extraction Guidance

- Store research plans before starting literature reviews or experiments
- Record outcomes — what was found, how it differed from hypothesis
- Store key findings with exact numbers and claims
- Track citation chains to understand intellectual lineage
- Record methodology details as observations, not just method names
- Link contradictory findings explicitly — high-value relationships
- Use `finding` entities for results you want to compare across papers
- Store venue info to track where communities publish
- When a paper makes a strong claim, store the exact quote as an observation
- Track which datasets are used by which methods for reproducibility
