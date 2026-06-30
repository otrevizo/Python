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

# Do LLM Agents Need a Semantic Layer?

### Experiment 2 — Semantic Layer Necessity

Oscar Trevizo
Harvard Extension School — Graduate Certificate in Data Science (2023)
Independent project · `machine_learning/agentic_semantic_layer_necessity.ipynb`

---

## The Question

Experiment 1 showed that model reasoning diverges on cross-metric questions.

All three models had the same tools, the same data, and the same semantic layer.

> **New question:** How much of that tool design matters?
> What if we remove the semantic layer entirely?

**The hypothesis:**

> LLM agents reason more accurately and consistently when querying data
> through semantic business names than when querying raw technical column names.

---

## What the Semantic Layer Provides

| Property | With Semantic Layer | Without Semantic Layer |
|---|---|---|
| **Column name** | `'net_migration_rate'` | `'NetMigrationRate_per_Kpop'` |
| **Discovery** | Named in system prompt | Must call `list_columns()` |
| **Alignment** | Matches model vocabulary | Requires technical guessing |
| **Error cost** | None — name resolves directly | Failed calls if name is wrong |
| **Unit** | Registered alongside name | Raw column, no metadata |

```python
# Condition A — governed access
query_product(business_name='net_migration_rate', year=2023, top_n=20)

# Condition B — raw access
list_columns(product_name='merged')
query_raw(column_name='NetMigrationRate_per_Kpop', year=2023, top_n=20)
```

---

## Experimental Design

| Element | Value |
|---|---|
| **Question** | *"Which country in the top 20 GDP has the highest migration rate?"* |
| **Models** | GPT-4o-mini · Haiku · Sonnet |
| **Condition A** | `query_product(business_name=...)` — semantic layer active |
| **Condition B** | `list_columns()` + `query_raw(column_name=...)` — no semantic layer |
| **Controlled** | Data, pipeline, merge, PRODUCT_REGISTRY, question |
| **Variable** | Presence or absence of the semantic layer |
| **Runs** | 6 total — 3 models × 2 conditions |
| **Verified answer** | Canada, +11.039 per 1,000 population (2023, UN WPP) |

---

## Results — At a Glance

| | Condition A (semantic layer) | Condition B (raw column names) |
|---|---|---|
| **GPT-4o-mini** | ❌ China, 357.14 (1964) | ❌ UAE, 128.43 (2007) |
| **Haiku** | ✅ Canada, 11.039 (2023) | ✅ Canada, 11.039 (2023) |
| **Sonnet** | ❌ Singapore, 41.83 (2007) | ❌ Singapore (same failure) |

**Correctness: 1/3 in both conditions.**

> The semantic layer did not change *who* got the right answer.
> But the tool call traces reveal something more important.

---

## GPT-4o-mini — Behavioral Profile

| | Condition A | Condition B |
|---|---|---|
| **Tool calls** | 6 | 10 |
| **Load order** | UN_WPP → WB_GDP | WB_GDP → UN_WPP |
| **Discovery** | `query_product` with business names | `list_columns` → failed guesses → `query_raw` |
| **Column guesses** | — | Tried `'gdp'`, `'net_migration_rate'` first (failed) |
| **Year filter** | None | None |
| **Answer** | China, 357.14 (1964) | UAE, 128.43 (2007) |

**Semantic leakage in Condition B:**
GPT-4o-mini first tried `query_raw(column_name='gdp')` and `query_raw(column_name='net_migration_rate')` —
the business names — as if they were raw column names. Both failed.
It then discovered `GDP_USD` and `NetMigrationRate_per_Kpop` from the error messages.

Without a year filter, historical extremes dominate: China 1964 (357.14), UAE 2007 (128.43).

---

## Haiku — Behavioral Profile

| | Condition A | Condition B |
|---|---|---|
| **Tool calls** | 8 | 9 |
| **Load order** | WB_GDP → UN_WPP | WB_GDP → UN_WPP |
| **Discovery** | Business names from system prompt | Tried `'gdp'` first (failed), recovered |
| **Column guesses** | — | One failed guess, then correct |
| **Round 1** | No year filter | No year filter |
| **Round 2** | `year=2023` applied | `year=2023` applied |
| **Answer** | ✅ Canada, 11.039 (2023) | ✅ Canada, 11.039 (2023) |

**Key observation:** Haiku also showed semantic leakage in Condition B — tried `'gdp'` as a raw
column name before recovering. But its recovery strategy (re-query with `year=2023`) was intact
in both conditions. The semantic layer saved one tool call; correctness was unchanged.

Haiku's WB_GDP-first load order is consistent across both experiments and both conditions.

---

## Sonnet — Behavioral Profile

| | Condition A | Condition B |
|---|---|---|
| **Tool calls** | 6 | 7 |
| **Load order** | UN_WPP → WB_GDP | UN_WPP → WB_GDP |
| **Discovery** | Business names from system prompt | `list_columns()` — chose correctly on first attempt |
| **GDP query** | `top_n=20`, no year filter | `top_n=20`, no year filter |
| **Migration query** | `top_n=200`, no year filter | `top_n=200`, no year filter |
| **Year filter** | Never applied | Never applied |
| **Answer** | ❌ Singapore, 41.83 (2007) | ❌ Singapore (same failure) |

**No semantic leakage in Condition B:** Sonnet called `list_columns()` first and chose
`GDP_USD` and `NetMigrationRate_per_Kpop` correctly on the first attempt.

Same failure mode in both conditions: without a year filter, `top_n=200` returns
historical peaks dominated by Gulf states and city-states. The semantic layer
was irrelevant to this failure.

---

## The Semantic Leakage Finding

> In Condition B, both GPT-4o-mini and Haiku tried to use business names
> as raw column names before discovering the technical column names.

```
GPT-4o-mini (Condition B):
  -> query_raw({'column_name': 'gdp', ...})          # ← semantic name, fails
  -> query_raw({'column_name': 'net_migration_rate'}) # ← semantic name, fails
  -> list_columns({'product_name': 'WORLD_BANK_GDP'}) # ← recovery
  -> query_raw({'column_name': 'GDP_USD', ...})        # ← correct raw name
```

**What this means:**

1. Business names are embedded in LLM training — models expect them even without instruction
2. The semantic layer aligns the tool interface to what models already know
3. Without it, models must pay a **discovery tax**: extra calls, failed attempts, error recovery

**Sonnet did not show leakage** — it called `list_columns()` first without guessing.
More disciplined discovery, but the same reasoning failure downstream.

---

## The Discovery Tax

Extra tool calls imposed by removing the semantic layer:

| Model | Condition A | Condition B | Extra calls | Source |
|---|---|---|---|---|
| GPT-4o-mini | 6 | 10 | **+4** | 2 failed column guesses + `list_columns` × 2 |
| Haiku | 8 | 9 | **+1** | 1 failed column guess |
| Sonnet | 6 | 7 | **+1** | `list_columns()` call |

The semantic layer eliminates guessing failures and the recovery overhead they create.
In a production system, each extra round-trip is latency + token cost + failure risk.

---

## The Core Failure Mode: Year Filter

All wrong answers in both conditions share one root cause:

```
Without year filter → query returns all-time peaks → wrong country wins

China, NetMigrationRate_per_Kpop = 357.14   (1964 — historical anomaly)
UAE,   NetMigrationRate_per_Kpop = 128.43   (2007 — oil boom peak)
Singapore, NetMigrationRate = 41.83         (2007 — financial hub growth)
```

**The semantic layer does not fix this.** Naming helps discovery.
It does not instruct the model to anchor to a specific year.

| Failure type | Caused by | Can semantic layer fix it? |
|---|---|---|
| Wrong column name | Discovery friction | **Yes** |
| Semantic name used as raw name | Model prior mismatch | **Yes — by alignment** |
| No year filter applied | Probabilistic reasoning | **No** |
| Wrong scope (top_n too wide/narrow) | Scope inference | **No** |

---

## Hypothesis Verdict

> **"LLM agents reason more accurately and consistently when querying data
> through semantic business names than when querying raw technical column names."**

| Claim | Result |
|---|---|
| **Correctness** | Same in both conditions (1/3). Naming did not determine correctness. |
| **Efficiency** | ✅ Confirmed. Every model needed more calls in Condition B. |
| **Alignment** | ✅ Confirmed. Semantic leakage proves models expect business names. |
| **Failure isolation** | ✅ Confirmed. Remaining failures are naming-independent reasoning errors. |

**Verdict: Partially confirmed — with important nuance.**

> The semantic layer is **necessary but not sufficient.**
> It eliminates the naming discovery tax and aligns tool interfaces to model priors.
> It cannot substitute for temporal reasoning (year filter) or scope inference (top_n strategy).

---

## Connection to Neurosymbolic AI

```
SYMBOLIC (Deterministic)              NEURAL (Probabilistic)
─────────────────────────             ──────────────────────────
SemanticLayer (business names)        LLM reasoning
Governed column resolution            Year filter decision
Discovery via business name           top_n scope inference
Error messages guide recovery         Cross-metric synthesis
```

**Condition A = full hybrid:** symbolic naming + neural reasoning
**Condition B = neural only on raw names:** discovery by guessing + same neural reasoning

Removing symbolic naming degraded efficiency and introduced alignment errors.
But the decisive variable was still neural reasoning quality.

> **Symbolic scaffolding reduces the space where neural failures can occur,
> but does not eliminate the probabilistic component.**

This is the core neurosymbolic finding from this experiment.

---

## Experiment 3 — Proposed

**The structural gap from Experiment 1 is still open:**

No tool returns *"migration rate filtered to the top-20 GDP countries."*
Models must bridge two separate query results through reasoning — that's where divergence enters.

**Proposed tool:**
```python
query_product_filtered_by(
    metric='net_migration_rate',
    filter_metric='gdp',
    filter_top_n=20,
    year=2023
)
```

**Hypothesis:** If the cross-metric join is governed and deterministic,
model divergence collapses to zero regardless of year filter behavior.

> See `machine_learning/agentic_model_reasoning_divergence.ipynb` — Experiment 1.

---

## Summary

```
Experiment 2:  Do LLMs need a semantic layer?
Same question · Same data · Same three models
Two conditions: with and without the semantic layer

Finding 1:  Correctness was 1/3 in both conditions.
            Naming did not determine who got the right answer.

Finding 2:  Discovery tax — Condition B cost every model extra tool calls.
            GPT-4o-mini: +4 calls. Haiku: +1. Sonnet: +1.

Finding 3:  Semantic leakage — GPT-4o-mini and Haiku tried to use business
            names as raw column names. The semantic layer matches model priors.

Finding 4:  The decisive failure is the year filter — a probabilistic reasoning
            choice the semantic layer cannot fix.

Verdict:    Semantic layer is necessary but not sufficient.
            It closes the naming gap. It cannot close the reasoning gap.
```

---

## References

- **Data:** UN WPP 2024 (population.un.org/wpp) · World Bank WDI (databank.worldbank.org)
- **Anthropic Tool Use:** docs.anthropic.com/en/docs/tool-use
- **OpenAI Function Calling:** platform.openai.com/docs/guides/function-calling
- **Data products:** Dehghani (2022) *Data Mesh*, O'Reilly
- **Experiment 1:** `machine_learning/agentic_model_reasoning_divergence.ipynb`
- **Experiment 2:** `machine_learning/agentic_semantic_layer_necessity.ipynb`
- **Support module:** `../python_vignettes/data_products/data_product_lib.py`

```
~/GitHub/Python/machine_learning/
  agentic_semantic_layer_necessity.ipynb        ← this experiment
  agentic_semantic_layer_necessity_slides.md    ← these slides
  agentic_model_reasoning_divergence.ipynb      ← Experiment 1
  agentic_model_reasoning_divergence_slides.md  ← Experiment 1 slides
```

*Render:* `marp agentic_semantic_layer_necessity_slides.md --html`
