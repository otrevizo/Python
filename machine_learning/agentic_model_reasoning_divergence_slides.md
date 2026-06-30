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

## GPT-4o-mini — 0 / 3 Correct, Different Failure Every Run

**Run 1** — migration first, no year → Hong Kong SAR (357.14) ❌
```
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})  ← FIRST
-> query_product({'business_name': 'gdp', 'top_n': 20})
```

**Run 2** — GDP first, no year → USA (2.84) ❌
```
-> query_product({'business_name': 'gdp', 'top_n': 20})                 ← fixed order
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})  ← still no year
```

**Run 3** — migration first, skipped GDP query entirely → Hong Kong SAR (357.14) ❌
```
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})  ← only query
```
*(6 tool calls total — GDP was never queried)*

Three runs. Three different tool sequences. One consistent failure: **no year filter.**
Without `year=2023`, queries return top-N across all years 1961–2023.
The model never inferred that "top 20 GDP" implies a specific year context.

---

## Haiku — Stochastic but Converging (2 / 3 Correct)

**Run 1** — GDP first, no year filter → confused, hedged Canada ⚠️
```
-> query_product({'business_name': 'gdp', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 100})  ← no year
```

**Run 2** — GDP first, added year=2023 → Canada, full ranked table ✅
```
-> query_product({'business_name': 'gdp', 'year': 2023, 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'year': 2023, 'top_n': 100})
```

**Run 3** — GDP first, added year=2023 → Canada ✅
```
-> query_product({'business_name': 'gdp', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'year': 2023, 'top_n': 50})  ← added
```

Run 1 was the outlier. Once Haiku discovered the year=2023 strategy in Run 2,
it applied it again in Run 3 — different top_n (50 vs 100) but same temporal anchor.
Capable, and converging toward reliability.

---

## Sonnet — Stable and Self-Optimising (3 / 3 Correct)

**Run 1 & 2** — GDP first, exploratory migration query, then year=2023 on both (9 calls)
```
-> query_product({'business_name': 'gdp', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})           ← explore
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20, 'year': 2023})
-> query_product({'business_name': 'gdp', 'top_n': 20, 'year': 2023})
```

**Run 3** — GDP first, migration year=2023 directly — no exploratory step (7 calls)
```
-> query_product({'business_name': 'gdp', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20, 'year': 2023})  ← direct
```

**Answer:** Canada — +11.04 per 1,000 (2023) ✅ in all three runs.

Sonnet skipped the exploratory unfiltered query in Run 3 — going straight to
`year=2023` on the first migration call. Same correct answer, fewer tool calls.
The temporal disambiguation strategy is stable and becoming more efficient.

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
