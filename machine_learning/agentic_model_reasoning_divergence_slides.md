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

## GPT-4o-mini — Wrong Order, Wrong Answer

```
-> list_available_sources({})
-> load_source({'source_name': 'UN_WPP'})
-> load_source({'source_name': 'WORLD_BANK_GDP'})
-> check_semantic_conflicts({...})
-> merge_sources({...})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})  ← FIRST
-> query_product({'business_name': 'gdp', 'top_n': 20})                 ← SECOND
```

**Answer:** China, Hong Kong SAR — 357.14 per 1,000 population ❌

**Failure mode:** Migration was queried before GDP, with no year filter.
The global migration top-20 spans all years 1961–2023.
Hong Kong SAR had extreme migration spikes in certain historical years —
a real data point, but from the wrong context.
The model never checked whether Hong Kong SAR is in the GDP top 20.
It is not.

---

## Haiku — Right Order, Reasoning Failure

```
-> list_available_sources({})
-> load_source({'source_name': 'WORLD_BANK_GDP'})
-> load_source({'source_name': 'UN_WPP'})
-> check_semantic_conflicts({...})
-> merge_sources({...})
-> query_product({'business_name': 'gdp', 'top_n': 20})                  ← correct order
-> query_product({'business_name': 'net_migration_rate', 'top_n': 100})  ← wide net
```

**Answer:** Confused — mentioned USA, UAE, Qatar, hedged on Canada ⚠️

**Failure mode:** Haiku queried GDP first (correct), then migration with a wider
net (top_n=100). But no tool returns "migration rate filtered to GDP top-20."
The agent had two separate result sets and could not cross-reference them in text.
It acknowledged the limitation mid-answer and guessed Canada by domain knowledge —
not from the data it retrieved.

---

## Sonnet — Temporal Filter, Correct Answer

```
-> list_available_sources({})
-> load_source({'source_name': 'UN_WPP'})
-> load_source({'source_name': 'WORLD_BANK_GDP'})
-> check_semantic_conflicts({...})
-> merge_sources({...})
-> query_product({'business_name': 'gdp', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20})
-> query_product({'business_name': 'net_migration_rate', 'top_n': 20, 'year': 2023})  ← added
-> query_product({'business_name': 'gdp', 'top_n': 20, 'year': 2023})                ← added
```

**Answer:** Canada — net migration rate +11.04 per 1,000 (2023) ✅

**What worked:** Sonnet issued 9 tool calls vs 7 for the others.
It added `year=2023` to both queries as a third reasoning step —
temporal disambiguation reduced the search space enough that the
cross-metric intersection became tractable in text.

---

## Results — Side by Side

| Model | Query order | Migration top_n | Year filter | Answer | Correct? |
|---|---|---|---|---|---|
| GPT-4o-mini | migration first | 20 | none | Hong Kong SAR (357.14) | NO |
| Haiku | GDP first | 100 | none | Confused / Canada (hedged) | PARTIAL |
| Sonnet | GDP first | 20 | 2023 | Canada (+11.04) | YES |

**Three models. Same tools. Same data. Three different outcomes.**

The divergence is not in the symbolic layer — it is in the neural reasoning
that bridges two separate query results.

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

**Supported.**

All three models diverged on this cross-metric question:

| Dimension | Diverged? | Evidence |
|---|---|---|
| Query order | Yes | GPT-4o-mini reversed it |
| Scope (top_n) | Yes | 20 vs 100 |
| Temporal filter | Yes | Sonnet added year=2023; others did not |
| Tool call count | Yes | 7 vs 7 vs 9 |
| Correctness | Yes | wrong / partial / correct |

Each failure is traceable to a specific reasoning decision at the cross-metric gap —
not to bad data, not to bad tools, not to a bad pipeline.

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
