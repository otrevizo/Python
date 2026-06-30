---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.1em;
  }
  code {
    font-size: 0.85em;
  }
  h1 { color: #2c3e50; }
  h2 { color: #34495e; }
  pre { background: #f4f4f4; }
  table { font-size: 0.9em; }
---

# Agentic Model Reasoning Divergence

### A Hypothesis Test: Do LLMs Diverge on Cross-Metric Questions?

Oscar Trevizo
Harvard Extension School — Graduate Certificate in Data Science (2023)
Independent project · `machine_learning/agentic_model_reasoning_divergence.ipynb`

---

## The Hypothesis

> **LLM agents diverge in reasoning strategy on questions that require
> filtering by one metric and ranking by another simultaneously.**

This divergence is not always visible in the final answer —
it is visible in the **tool call sequence**.

**The experiment:**
Run the same question through three models.
Same tools. Same data. Same registry.
The only variable: the model.

---

## Why Cross-Metric Questions Are Hard

**Single-metric question** (easy — one tool call answers it):
> *"Which country has the highest migration rate?"*
→ `query_product(business_name='net_migration_rate', top_n=1)`

**Cross-metric question** (hard — two result sets must be joined in reasoning):
> *"Which country **in the top 20 GDP** has the highest migration rate?"*
→ No single tool answers this. The agent must:
  1. Query top-20 by GDP
  2. Query migration rates
  3. **Mentally intersect the two lists**

Step 3 happens inside the model — not in any tool.
That is where divergence enters.

---

## Experimental Design

| Element | Value |
|---|---|
| **Question** | *"Which country in the top 20 GDP has the highest migration rate?"* |
| **Phrasing** | Vague — no explicit two-step instruction |
| **Data** | UN WPP 2024 · World Bank WDI (GDP) |
| **Tools** | 8 tools: list, load, check, rename, merge, query, card, lineage |
| **Models** | GPT-4o-mini · Haiku · Sonnet |
| **Controlled** | Symbolic scaffolding — identical across all runs |
| **Variable** | LLM reasoning — model only |

**What we measure:**
- Tool call sequence and query order
- `top_n` chosen for the migration rate query
- Whether a year filter was applied
- Final answer and correctness

---

## GPT-4o-mini — 0 / 3 Correct

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| **Tool calls** | 7 | 7 | 6 |
| **Load order** | UN_WPP → WB_GDP | UN_WPP → WB_GDP | UN_WPP → WB_GDP |
| **Product name** | GDP_Migration_Data | GDP_Migration_Data | Merged_GDP_and_Migration |
| **Query 1** | migration (top_n=20) | gdp (top_n=20) | migration (top_n=20) |
| **Query 2** | gdp (top_n=20) | migration (top_n=20) | *(stopped — no GDP query)* |
| **Year filter** | none | none | none |
| **Answer** | Hong Kong SAR (357.14) | USA (2.84) | Hong Kong SAR (357.14) |

**What varied:** Query order flipped between runs. Product name changed in Run 3.
Tool call count dropped by 1 in Run 3.

**What was consistent:** Load order always UN_WPP first. No year filter ever.

**Run 3 detail:** The model loaded and merged the World Bank GDP data — it was
in the registry and ready to use. It then queried only migration rate and stopped.
It reported Hong Kong SAR without checking whether it is in the GDP top 20.
It trusted prior knowledge instead of querying the data it had just prepared.

---

## Haiku — 2 / 3 Correct, Converging

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| **Tool calls** | 7 | 9 | 8 |
| **Load order** | WB_GDP → UN_WPP | WB_GDP → UN_WPP | WB_GDP → UN_WPP |
| **Product name** | GDP_MIGRATION | gdp_migration | gdp_migration |
| **Query 1** | gdp (top_n=20) | gdp (top_n=20) | gdp (top_n=20) |
| **Query 2** | migration (top_n=100) | migration (top_n=20) | migration (top_n=20) |
| **Query 3** | *(stopped)* | gdp (year=2023, top_n=20) | migration (year=2023, top_n=50) |
| **Query 4** | | migration (year=2023, top_n=100) | *(stopped)* |
| **Year filter** | none | 2023 on both metrics | 2023 on 2nd migration query only |
| **Answer** | Confused / hedged Canada | Canada — full ranked table | Canada |

**What varied:** Tool call count (7→9→8). Product name casing changed after Run 1.
top_n for migration differed each run (100, 20+100, 20+50). Run 2 re-queried both
metrics with year=2023; Run 3 re-queried only migration.

**What was consistent:** Load order always WB_GDP first — unique among the three models
(GPT-4o-mini and Sonnet always loaded UN_WPP first). GDP always queried before migration.

**The convergence:** Run 1 had no year filter and failed. Once the year=2023 strategy
appeared in Run 2 it held in Run 3. Run 1 was the outlier; Runs 2–3 show a pattern.

---

## Sonnet — 3 / 3 Correct, Self-Optimising

| | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| **Tool calls** | 9 | 9 | 7 |
| **Load order** | UN_WPP → WB_GDP | UN_WPP → WB_GDP | UN_WPP → WB_GDP |
| **Product name** | gdp_migration_product | population_gdp_product | gdp_migration_product |
| **Query 1** | gdp (top_n=20) | gdp (top_n=20) | gdp (top_n=20) |
| **Query 2** | migration (top_n=20) | migration (top_n=20) | migration (year=2023, top_n=20) |
| **Query 3** | migration (year=2023, top_n=20) | migration (year=2023, top_n=20) | *(stopped)* |
| **Query 4** | gdp (year=2023, top_n=20) | gdp (year=2023, top_n=20) | |
| **Year filter** | added in queries 3 & 4 | added in queries 3 & 4 | applied directly in query 2 |
| **Answer** | Canada +11.04 | Canada +11.04 | Canada +11.04 |

**What varied:** Product name stochastic (gdp_migration_product / population_gdp_product / gdp_migration_product).
Tool calls dropped from 9 to 7 in Run 3. Exploratory unfiltered migration query
present in Runs 1–2, skipped in Run 3.

**What was consistent:** Load order always UN_WPP first. GDP always queried first.
year=2023 applied every run. Answer identical across all three runs.

**The optimisation:** Runs 1–2 issued an exploratory migration query without year filter,
then re-queried with year=2023. Run 3 went straight to year=2023 on the first migration
call — 2 fewer tool calls, same correct answer. The strategy is stable and tightening.

---

## Results — Three Runs

| Model | Run 1 | Run 2 | Run 3 | Correct rate |
|---|---|---|---|---|
| GPT-4o-mini | NO (HK SAR, bad order) | NO (USA, no year) | NO (HK SAR, skipped GDP) | **0 / 3** |
| Haiku | PARTIAL (hedged) | YES (full table) | YES (Canada) | **2 / 3** |
| Sonnet | YES (Canada) | YES (Canada) | YES (Canada, fewer calls) | **3 / 3** |

**Nine runs total. Same tools. Same data. Divergence confirmed across all three.**

Key observations:
- GPT-4o-mini: no year filter in any run — the consistent failure
- Haiku: found the year=2023 strategy in Run 2, applied it in Run 3
- Sonnet: stable and got more efficient (9 → 9 → 7 tool calls)

---

## Stability Across Three Runs

| Model | Run 1 | Run 2 | Run 3 | Correct rate |
|---|---|---|---|---|
| GPT-4o-mini | Wrong | Wrong | Wrong | 0 / 3 |
| Haiku | Partial | Correct | Correct | 2 / 3 |
| Sonnet | Correct | Correct | Correct | 3 / 3 |

**GPT-4o-mini** never added a year filter in any run. Query order was stochastic
(migration-first in Runs 1 and 3; GDP-first in Run 2) but that is not the root cause.
Run 3 regressed further — it skipped the GDP query entirely with only 6 tool calls.

**Haiku** converged. Run 1 was the outlier — no year filter, confused reasoning.
Runs 2 and 3 both applied year=2023 and reached the correct answer.
Stochastic at the start; converging toward reliability.

**Sonnet** was stable and self-optimising. Correct in all three runs.
Runs 1 and 2 used 9 tool calls with an exploratory unfiltered migration query.
Run 3 went straight to `year=2023` — 7 tool calls, same correct answer.

---

## The Structural Gap

No tool in the registry can answer the question directly:

> *"Return migration rate, sorted descending,*
> *filtered to only the top-20 GDP countries."*

Every model had to bridge two `query_product()` result sets in its own reasoning.

```
query(gdp, top_n=20)           → list A: top-20 GDP countries
query(migration, top_n=?)      → list B: top-? migration countries

                    A ∩ B = ?
                 (no tool for this)
                 (the model must reason it)
```

This gap is not a bug — it reflects the real architecture of governed data products.
Tools return governed, auditable data. Reasoning is the model's job.
When the reasoning fails, the symbolic layer preserves the trace but cannot fix the answer.

---

## Hypothesis Verdict

**Supported across all three runs.**

| Dimension | Diverged? | Evidence |
|---|---|---|
| Query order | Yes | GPT-4o-mini stochastic; Haiku/Sonnet GDP-first |
| Temporal filter | Yes | Sonnet every run; Haiku Runs 2–3; GPT-4o-mini never |
| Tool call count | Yes | 6 to 9 across models and runs |
| Correctness | Yes | 0/3 · 2/3 · 3/3 |

Each failure is traceable to a specific reasoning decision at the cross-metric gap —
not to bad data, not to bad tools, not to a bad pipeline.

Three runs reveal two kinds of divergence:
- **Cross-model divergence** — models differ in strategy and correctness
- **Within-model variance** — the same model produces different strategies across runs

GPT-4o-mini is stochastic and consistently wrong.
Haiku is stochastic but converging toward the correct strategy.
Sonnet is stable, correct, and self-optimising.

---

## Neurosymbolic Implication

The symbolic scaffolding worked identically for all three models:

- Data loaded correctly ✅
- Semantic layer resolved column names ✅
- Collision check passed ✅
- Merge executed correctly ✅
- Lineage tracked ✅

The **tools returned correct data**. The **reasoning determined the answer**.

> A governed wrong answer is still a wrong answer.
> The symbolic layer makes it **traceable**.
> The neural layer makes it **true — or not**.

This is the core claim of the neurosymbolic governance hypothesis:
**symbolic structure is necessary but not sufficient.**
The neural component must also be capable of cross-metric inference.

---

## Next Steps

| Extension | What it tests |
|---|---|
| Repeat N times per model | Measure variance — is divergence stable or stochastic? |
| Add cross-filter tool | Does the gap close if tools handle the intersection? |
| Explicit two-step phrasing | Does prompt specificity eliminate divergence? |
| Third data source | Does source-selection judgment change model ranking? |
| Stronger models (GPT-4o, Opus) | Is divergence a capability gap or a reasoning style? |

**Immediate next step:**
Add a `query_product_filtered_by` tool that accepts a secondary filter set —
and rerun the experiment to see if the structural gap, when closed symbolically,
eliminates the divergence entirely.

If it does: the hypothesis refines to
*"divergence occurs at unmediated cross-metric gaps — add a tool, close the gap."*

---

## Code and Data

```
~/GitHub/Python/machine_learning/
  agentic_model_reasoning_divergence.ipynb   ← experiment notebook
  agentic_model_reasoning_divergence_slides.md ← these slides

~/GitHub/Python/python_vignettes/data_products/
  data_product_lib.py                        ← 4 classes (symbolic layer)
  agentic_data_product_vignette.ipynb        ← prior work: single-model agent
  data_products_agent_slides.md              ← prior slides: what we built
```

*Render with Marp CLI or the VS Code Marp extension.*
`marp agentic_model_reasoning_divergence_slides.md --html`

---

## References

- **Data:** UN WPP 2024 (population.un.org/wpp) · World Bank WDI (databank.worldbank.org)
- **Anthropic Tool Use:** docs.anthropic.com/en/docs/tool-use
- **OpenAI Function Calling:** platform.openai.com/docs/guides/function-calling
- **Data products:** Dehghani (2022) *Data Mesh*, O'Reilly
- **Neurosymbolic AI:** Garcez & Lamb (2023) *Neurosymbolic AI: The 3rd Wave*
- **Prior slides:** `python_vignettes/data_products/data_products_agent_slides.md`
