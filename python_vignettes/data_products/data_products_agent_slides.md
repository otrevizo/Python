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
---

# Governed Data Products + Agentic AI

### A Hybrid Architecture for Dynamic Data Composition

Oscar Trevizo
Harvard Extension School — Graduate Certificate in Data Science (2023)
Independent project · `python_vignettes/data_products/`

---

## The Problem

**Three separate realities:**

1. Data lives in **multiple sources** with different schemas, column names, and units
2. Questions **span sources** — *"Which top-20 GDP country had the highest migration rate in 2023?"*
3. Combining sources correctly requires **a human data steward** every time

> Every ad-hoc join is ungoverned, undocumented, and unrepeatable.

**Goal:** Make composition governed, self-describing, and — eventually — dynamic.

---

## What Is a Data Product?

*Zhamak Dehghani — Data Mesh (O'Reilly, 2022)*

A data product is a **unit of data** that is:

| Property | Meaning |
|---|---|
| **Discoverable** | Has a name, description, domain, owner |
| **Self-describing** | Schema + semantic layer (business names) |
| **Quality-governed** | Row count, completeness, freshness |
| **Lineage-tracked** | Every transformation is logged |

> Not a table. Not a file. A *governed artifact* with a contract.

---

## `data_product_lib.py` — Four Classes

A custom local module (not a published package) built for this series.

```python
DataProductMetadata   # name, owner, source, license, version, refresh frequency
SemanticLayer         # business-name → raw column registry
LineageTracker        # append-only log of pipeline steps
DataProduct           # wraps a DataFrame with the three above
                      # exposes .schema() .quality() .card() .contract()
```

**Conceptual origins:**
- `DataProductMetadata` → Dehghani, Data Mesh
- `SemanticLayer` → dbt Semantic Layer / Looker LookML
- `LineageTracker` → OpenLineage / DataHub
- `DataProduct` → datacontract.com

---

## Data Product 1 — UN World Population Prospects

**Source:** UN WPP 2024 · CC BY 3.0 IGO · Every 2 years

```
WPP Excel (Estimates sheet)
        ↓  load_un_wpp()     — skiprows=16, 11 column renames
        ↓  filter_countries() — LocType == 'Country' only
        ↓  clean_types()      — pd.to_numeric on 7 columns
        ↓
     DP1: 14,931 rows × 14 cols
          237 countries × 1961–2023
```

**Semantic layer (5 entries):**
`net_migration_rate` · `net_migrants` · `population` · `fertility_rate` · `life_expectancy`

**Lineage:** 3 steps logged · Parquet + contract JSON exported to `output/`

---

## Data Product 2 — World Bank GDP

**Source:** World Bank WDI · CC BY 4.0 · Annual

```
WB_GDP.xls + WB_GDP_growth.xls  (wide format, 1960–2025)
        ↓  load_wb_gdp()
           — skiprows=3, wide → long (stack)
           — ISO3 as index (robust join key vs country name)
           — two indicators merged on ISO3 + Year
        ↓
     DP2: ~16,000 rows × 3 cols
          266 ISO3 codes × 1961–2023
```

**Semantic layer (2 entries):**
`gdp` (NY.GDP.MKTP.KD) · `gdp_growth` (NY.GDP.MKTP.KD.ZG)

**Lineage:** 1 step logged

---

## DP3 = DP1 ⊕ DP2 — Composition

```
     DP1 (Demographics)          DP2 (Economics)
     14,931 rows × 14 cols       ~16,000 rows × 3 cols
     5 semantic entries          2 semantic entries
     3 lineage steps             1 lineage step
              │                        │
              └──────── merge ─────────┘
                   on: ISO3 + Year
                   how: inner join
                        │
                     DP3 (Multi-domain)
                     10,920 rows × 16 cols
                     210 countries × 1961–2023
                     7 semantic entries (5 + 2)
                     5 lineage steps  (3 + 1 + 1 merge)
```

**Join key: ISO3** — more robust than country name (no spelling mismatches)

---

## The Collision Check

Before merging, the semantic layers are compared:

```python
collisions = set(dp1.semantic_layer) & set(dp2.semantic_layer)
if collisions:
    raise ValueError(f'Semantic name collision(s): {sorted(collisions)}')
```

**Why it matters:**

If both sources define `"population"` differently, a silent overwrite
produces a product where a business name resolves to the wrong column —
no error, wrong answer downstream.

> A collision is not a merge error. It is a **governance failure.**
> Detect it before it becomes an invisible data quality bug.

---

## Why an Agent?

**Hardcoded pipeline:**
```python
dp1 = build_wpp()
dp2 = build_wb()
dp3 = merge(dp1, dp2)
answer = dp3.query("net_migration_rate", year=2023)
```
Works for this question. Breaks the moment the goal changes.

**Agentic pipeline:**
```
User: "Build a demographics + economics product for 2000–2019"
Agent: decides which sources, loads them, checks conflicts,
       merges, queries — from the goal, not a script
```

The agent adds value precisely where hardcoding fails:
**dynamic source selection, semantic conflict resolution, natural language goals.**

---

## The Agent Loop

```
User question
      ↓
  Claude reasons ──────────────────────────────┐
      ↓                                        │
  tool_use: call a Python function             │
      ↓                                        │
  tool_result: JSON returned to Claude         │
      ↓                                        │
  Claude reasons again ────────────────────────┘
      ↓ (stop_reason == "end_turn")
  Text answer returned
```

**State lives in `PRODUCT_REGISTRY`** — a Python dict that persists across
tool calls within the session. Load once, query many times.

`AGENT_MODEL` variable controls Haiku vs Sonnet without touching the loop.

---

## Eight Tools

| Tool | What it does |
|---|---|
| `list_available_sources` | Catalogue of loadable sources |
| `load_source` | Load + register a DataProduct |
| `check_semantic_conflicts` | Detect name collisions before merge |
| `rename_semantic_entry` | Resolve a conflict by renaming |
| `merge_sources` | Inner join two DataProducts |
| `query_product` | Semantic-name query (business → column) |
| `get_product_card` | Human-readable summary |
| `get_lineage` | Full audit trail |

The agent calls these in the order it chooses based on the goal.
The order is not hardcoded — it is reasoned.

---

## Agent in Action — A Real Question

**Question:** *"Which country in the top 20 GDP has the highest migration rate?"*

**Agent tool calls (Sonnet, explicit two-step phrasing):**

```
→ list_available_sources({})
→ load_source({'source_name': 'UN_WPP'})
→ load_source({'source_name': 'WORLD_BANK_GDP'})
→ check_semantic_conflicts({'source1_name': 'UN_WPP', ...})
→ merge_sources({...,'product_name': 'MERGED'})
→ query_product({'business_name': 'gdp', 'top_n': 20, 'year': 2023})
→ query_product({'business_name': 'net_migration_rate', 'top_n': 210, 'year': 2023})
```

**Answer:** Canada — 11.039 per 1,000 population (2023)

*Verified against raw UN WPP Excel file: 11.039 is in the source unchanged.*

---

## Same Question, Different Strategies

The model's reasoning path — not just the answer — varies.

| Run | Model | Migration query | Output |
|---|---|---|---|
| Run 1 | Haiku | `top_n=20` (intersection) | Canada + Saudi Arabia only |
| Run 2 | Haiku | `top_n=100` (wide net) | Full table of 20 countries |
| Run 3 | Sonnet (vague) | `top_n=20` (intersection) | Canada + Saudi Arabia only |
| Run 4 | Sonnet (explicit) | `top_n=210` (all countries) | Full ranked table |

**The answer (Canada) was consistent. The path was not.**

Agent reasoning variance is real and observable from the tool call traces.

---

## Prompt Specificity Changes Tool Strategy

**Vague:** *"Which country in the top 20 GDP has the highest migration rate?"*
→ Agent infers scope → `top_n=20` intersection → misses most of the table

**Explicit two-step:** *"Get the top 20 countries by GDP. For just those 20 countries, which has the highest net migration rate?"*
→ Agent follows steps → `top_n=210` then filter → full ranked table

> This is not a failure to fix with better tools.
> It is the fundamental tension between how humans ask questions
> and what tools can compute directly.
> The gap is filled by LLM reasoning — which is probabilistic.

---

## The Result — Top 20 GDP, Ranked by Migration (2023)

| # | Country | GDP Rank | Net Migration Rate |
|---|---|---|---|
| 1 | 🇨🇦 Canada | #11 | **+11.04** |
| 2 | 🇸🇦 Saudi Arabia | #19 | +9.79 |
| 3 | 🇳🇱 Netherlands | #18 | +7.99 |
| 4 | 🇩🇪 Germany | #4 | +7.21 |
| 5 | 🇦🇺 Australia | #12 | +5.30 |
| … | … | … | … |
| 16 | 🇨🇳 China | #2 | −0.40 |
| 19 | 🇧🇷 Brazil | #9 | −1.14 |
| 20 | 🇹🇷 Türkiye | #16 | −3.65 |

**13 of 20 top economies are net immigration destinations.**
GDP size does not predict migration attractiveness (Switzerland #20 GDP, #7 migration).

---

## The Bigger Picture — Why This Matters

Two systems working together in this vignette:

```
SYMBOLIC (Deterministic)          NEURAL (Probabilistic)
─────────────────────────         ─────────────────────────
DataProduct classes               LLM Agent (Claude)
Semantic layer rules              Natural language goals
Collision detection               Conflict resolution
Lineage tracking                  Cross-metric reasoning
Data contracts                    Source selection
Schema validation                 Scope inference
```

**Neither is sufficient alone.**

- LLM alone → unverifiable outputs, no lineage, no governance
- Rules alone → brittle to new questions, requires hardcoded logic for every case

---

## Neurosymbolic AI + Governance — The Hypothesis

> Hybrid systems that combine symbolic governance structures
> with neural reasoning — and keep humans in the loop —
> are necessary for reliable, auditable data intelligence.

**Evidence from this exercise:**

| Claim | Evidence |
|---|---|
| Symbolic alone is brittle | Hardcoded pipeline can't answer novel questions |
| Neural alone is unverifiable | Agent output without lineage cannot be audited |
| Governance requires structure | SemanticLayer + LineageTracker make the agent's work inspectable |
| Humans must remain in the loop | AGENT_MODEL selector, verification cell, rename tool |
| Transparency is not the same as correctness | Tool traces show reasoning; raw data check confirms accuracy |

---

## What Governance Looks Like in Practice

**In this vignette, governance is not an afterthought — it is structural:**

- `SemanticLayer` → every column has a business name, unit, and source system
- `LineageTracker` → every transformation is logged with input/output shape
- Collision check → fails fast rather than silently overwriting
- `rename_semantic_entry` → human-interpretable conflict resolution
- Verification cell → raw source checked against pipeline output
- `AGENT_MODEL` → model is a visible, changeable parameter
- Tool call traces → agent reasoning is auditable in real time

> The agent cannot produce a governed output by itself.
> It needs the symbolic scaffolding to do so.

---

## Known Limitations and Next Extensions

**Current limitations:**
- `SOURCE_CONFIGS` has only 2 sources — agent has no real source-selection decision to make
- UN WPP rate is a demographic residual, not the same as country headline immigration statistics

**Natural next steps:**

| Extension | What it adds |
|---|---|
| Third source (WB CO₂, UN Migration Stock) | Real source-selection judgment by the agent |
| DP4 = DP3 ⊕ third source | Deeper composition, longer lineage |
| Multimodal governance | Text reports + structured data as co-equal sources |

→ **The model-agnostic experiment was built and run — see next slide.**

---

## Next Experiment — Model Reasoning Divergence

The model-agnostic loop was built and run as a separate hypothesis test.

**Hypothesis:** LLM agents diverge on cross-metric reasoning questions —
specifically when the answer requires filtering by one metric and ranking
by another simultaneously.

**Same question. Same tools. Same data. Three models.**

| Model | Strategy | Correct? |
|---|---|---|
| GPT-4o-mini | intersection — migration queried first | NO (returned Hong Kong SAR) |
| Haiku | filter-then-rank (top_n=100) — could not cross-reference | PARTIAL |
| Sonnet | intersection + year=2023 filter on both queries | YES (Canada, +11.04) |

**Finding:** All three models diverged in query order, scope, and correctness.
The symbolic scaffolding returned identical correct data to all three.
The neural reasoning determined the outcome.

> See `machine_learning/agentic_model_reasoning_divergence.ipynb`
> and `agentic_model_reasoning_divergence_slides.md`

---

## Summary

```
Raw sources (Excel / API)
        ↓
  Governed Data Products        ← symbolic structure
  (metadata · semantics ·
   quality · lineage)
        ↓
  PRODUCT_REGISTRY              ← stateful data catalog
        ↓
  LLM Agent (Claude)            ← neural reasoning
  8 tools · tool-use loop
        ↓
  Natural language answer       ← grounded in governed data
  + audit trail
```

The hypothesis: **governed hybrid systems > pure neural OR pure symbolic.**
This vignette is a small but concrete demonstration of that claim.

---

## References

- Dehghani, Z. (2022). *Data Mesh.* O'Reilly Media.
- Fowler, M. *Data Mesh Principles.* martinfowler.com
- *UN World Population Prospects 2024.* population.un.org/wpp · CC BY 3.0 IGO
- *World Bank World Development Indicators.* databank.worldbank.org · CC BY 4.0
- *Anthropic Tool Use.* docs.anthropic.com/en/docs/tool-use
- *OpenLineage.* openlineage.io — lineage tracking pattern
- *dbt Semantic Layer.* docs.getdbt.com — semantic naming pattern
- *datacontract.com* — data contract specification

---

## Code

All notebooks and the `data_product_lib.py` module:

```
~/GitHub/Python/python_vignettes/data_products/
  data_product_lib.py                 ← 4 classes
  data_product_lib_vignette.ipynb     ← synthetic tutorial
  un_wpp_data_product.ipynb           ← DP1
  un_wpp_wb_data_product.ipynb        ← DP3 = DP1 ⊕ DP2
  agentic_data_product_vignette.ipynb ← agent loop (single model)
  data_product_lib_tutorial.md        ← API reference
  data_products_agent_slides.md       ← these slides

~/GitHub/Python/machine_learning/
  agentic_model_reasoning_divergence.ipynb       ← three-model experiment
  agentic_model_reasoning_divergence_slides.md   ← experiment slides
```

*Render with Marp CLI or the VS Code Marp extension.*
`marp data_products_agent_slides.md --html`
