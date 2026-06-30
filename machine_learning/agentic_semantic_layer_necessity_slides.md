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
| **Runs** | 12 total — 3 models × 2 conditions × 2 runs |
| **Verified answer** | Canada, +11.039 per 1,000 population (2023, UN WPP) |

---

## Results — At a Glance (2 runs)

| | Cond A Run 1 | Cond A Run 2 | Cond B Run 1 | Cond B Run 2 |
|---|---|---|---|---|
| **GPT-4o-mini** | ❌ China (1964) | ❌ Kuwait (1991) | ❌ UAE (2007) | ❌ UAE (2023) |
| **Haiku** | ✅ Canada | ✅ Canada | ✅ Canada | ✅ Canada |
| **Sonnet** | ❌ Singapore | ✅ Canada | ❌ Singapore | ✅ Canada |

**Cumulative correctness:** GPT-4o-mini 0/4 · Haiku 4/4 · Sonnet 2/4

> The semantic layer did not change *who* got the right answer.
> Sonnet's correction in Run 2 confirms its year filter decision is probabilistic.
> But the tool call traces reveal something more important.

---

## GPT-4o-mini — Behavioral Profile (0/4 correct)

| | Cond A Run 1 | Cond A Run 2 | Cond B Run 1 | Cond B Run 2 |
|---|---|---|---|---|
| **Tool calls** | 6 | 7 | 10 | 8 |
| **Merge step** | ✅ | ❌ skipped | ✅ | ❌ skipped |
| **Semantic leakage** | — | — | ✅ tried 'gdp' | ❌ none |
| **Year filter** | None | None | None | Migration only |
| **Answer** | China (1964) | Kuwait (1991) | UAE (2007) | UAE (2023) |

**Two distinct failure modes — both probabilistic:**

**1. No year filter:** Without `year=2023`, all-time peaks dominate — China 1964 (357.14), Kuwait 1991 (340.85).

**2. Skipped merge (Run 2, both conditions):** Queried source products separately, then reasoned
across disconnected result sets. UAE appeared at top of 2023 UN_WPP migration — but UAE is not in
the top-20 GDP list the model had seen from a separate WORLD_BANK_GDP query.

**Semantic leakage is also probabilistic** — present in Run 1, absent in Run 2.

---

## Haiku — Behavioral Profile (4/4 correct)

| | Cond A Run 1 | Cond A Run 2 | Cond B Run 1 | Cond B Run 2 |
|---|---|---|---|---|
| **Tool calls** | 8 | 8 | 9 | 7 |
| **Load order** | WB_GDP → UN_WPP | UN_WPP → WB_GDP | WB_GDP → UN_WPP | WB_GDP → UN_WPP |
| **Merge step** | ✅ | ✅ | ✅ | ✅ |
| **Semantic leakage** | — | — | ✅ tried 'gdp' | ✅ tried 'gdp' |
| **Year filter** | Round 2 | Round 2 | Round 2 | Applied directly |
| **Answer** | ✅ Canada | ✅ Canada | ✅ Canada | ✅ Canada |

**Most reliable model across all conditions and runs.**

Two-round strategy (broad first → year-filtered second) is consistent across Condition A.
In Condition B Run 2, applied `year=2023` directly — more efficient (7 calls vs 9).

**Semantic leakage is consistent in Condition B** — tried `'gdp'` as a raw column name in
both runs, recovered via error message each time. The semantic layer aligns to Haiku's priors.

Load order is not perfectly stable (UN_WPP-first appeared in Condition A Run 2) but correctness
was unaffected — merge order does not change the inner join result.

---

## Sonnet — Behavioral Profile (2/4 correct)

| | Cond A Run 1 | Cond A Run 2 | Cond B Run 1 | Cond B Run 2 |
|---|---|---|---|---|
| **Tool calls** | 6 | 8 | 7 | 9 |
| **Merge step** | ✅ | ✅ | ✅ | ✅ |
| **Semantic leakage** | — | — | ❌ none | ❌ none |
| **Round 1** | top_n=200, no year | top_n=20, no year | top_n=200, no year | top_n=200, no year |
| **Round 2** | — (stopped) | top_n=20, year=2023 ✅ | — (stopped) | top_n=500, year=2023 ✅ |
| **Year filter** | Never | Round 2 | Never | Round 2 |
| **Answer** | ❌ Singapore (2007) | ✅ Canada (2023) | ❌ Singapore (2007) | ✅ Canada (2023) |

**Year filter decision is probabilistic — the decisive variable.**

In both runs where Sonnet was wrong, it stopped after one wide query with no year filter.
In both runs where it was correct, it added a second round with `year=2023`.
The failure mode and the correction are identical across conditions — the semantic layer
was irrelevant to both.

**No semantic leakage in Condition B** — Sonnet calls `list_columns()` and picks correct
raw column names on the first attempt, in both runs. Most disciplined discovery of the three models.

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

**Leakage is model-dependent and probabilistic across 2 runs:**

| Model | Run 1 leakage | Run 2 leakage | Pattern |
|---|---|---|---|
| GPT-4o-mini | ✅ | ❌ | Probabilistic |
| Haiku | ✅ | ✅ | Consistent |
| Sonnet | ❌ | ❌ | Never |

**Sonnet never shows leakage** — calls `list_columns()` and picks correctly both runs.

---

## The Discovery Tax (averaged across 2 runs)

Extra tool calls imposed by removing the semantic layer:

| Model | Cond A avg | Cond B avg | Extra calls | Pattern |
|---|---|---|---|---|
| GPT-4o-mini | 6.5 | 9.0 | **+2.5** | Leakage probabilistic; skipped merge in Run 2 |
| Haiku | 8.0 | 8.0 | **0** | Leakage consistent, but recovery very fast |
| Sonnet | 7.0 | 8.0 | **+1** | `list_columns()` call only — no leakage |

**The tax is real but smaller than Run 1 suggested.**

Haiku's discovery overhead dropped to zero on average because Run 2 was more efficient.
GPT-4o-mini's overhead is inflated by the skipped-merge failure in Run 2, not just leakage.

The semantic layer eliminates guessing failures and recovery overhead —
in a production system, each extra round-trip is latency + token cost + failure risk.

---

## The Core Failure Modes (2 runs)

All wrong answers across both runs share two independent root causes:

**1. No year filter — all-time peaks dominate:**
```
China    (1964)  357.14 per 1,000  ← historical anomaly
Kuwait   (1991)  340.85 per 1,000  ← Gulf War displacement
UAE      (2007)  128.43 per 1,000  ← oil boom peak
Singapore(2007)   41.83 per 1,000  ← financial hub growth
```

**2. Skipped merge (GPT-4o-mini Run 2, both conditions):**
Queried sources separately → cross-dataset comparison in LLM reasoning →
UAE led the UN_WPP migration list but was absent from the GDP list seen.

| Failure type | Probabilistic? | Can semantic layer fix it? |
|---|---|---|
| Wrong column name | Yes (leakage) | **Yes — by alignment** |
| No year filter | Yes — Sonnet corrected in Run 2 | **No** |
| Skipped merge step | Yes — new in Run 2 | **No** |
| Wrong scope (top_n) | Yes | **No** |

---

## Hypothesis Verdict

> **"LLM agents reason more accurately and consistently when querying data
> through semantic business names than when querying raw technical column names."**

| Claim | Result |
|---|---|
| **Correctness** | Same across conditions — naming did not determine correctness in either run. |
| **Efficiency** | Confirmed in Run 1; reduced in Run 2 — Haiku closed the gap completely. |
| **Alignment** | Partially — Haiku shows consistent leakage; GPT-4o-mini probabilistic; Sonnet never. |
| **Failure isolation** | ✅ Confirmed — year filter and skipped merge are naming-independent. |

**Verdict: Necessary but not sufficient — and the gap is smaller than Run 1 suggested.**

> The semantic layer is **necessary but not sufficient.**
> It eliminates the naming discovery tax and aligns tool interfaces to model priors.
> It cannot fix year filter failures, skipped merge steps, or scope inference errors.

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

## Summary (2 runs)

```
Experiment 2:  Do LLMs need a semantic layer?
Same question · Same data · Same three models · 2 runs
Two conditions: with and without the semantic layer

Finding 1:  Correctness — GPT-4o-mini 0/4, Haiku 4/4, Sonnet 2/4.
            Naming did not determine who got the right answer.

Finding 2:  Discovery tax — real but variable. Averaged across 2 runs:
            GPT-4o-mini +2.5 calls, Haiku 0, Sonnet +1.

Finding 3:  Semantic leakage is model-dependent and probabilistic.
            Haiku: consistent. GPT-4o-mini: Run 1 only. Sonnet: never.

Finding 4:  Two independent failure modes — year filter and skipped merge —
            both probabilistic, both naming-independent.

Finding 5:  Sonnet corrected itself in Run 2 (wrong → correct, both conditions).
            The year filter decision is the decisive probabilistic variable.

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
