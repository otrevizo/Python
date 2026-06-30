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
| **Runs** | 18 total — 3 models × 2 conditions × 3 runs |
| **Verified answer** | Canada, +11.039 per 1,000 population (2023, UN WPP) |

---

## Results — At a Glance (3 runs)

| | Cond A R1 | Cond A R2 | Cond A R3 | Cond B R1 | Cond B R2 | Cond B R3 |
|---|---|---|---|---|---|---|
| **GPT-4o-mini** | ❌ China | ❌ Kuwait | ❌ UAE | ❌ UAE | ❌ UAE | ❌ inconclusive |
| **Haiku** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Sonnet** | ❌ Singapore | ✅ | ❌ USA | ❌ Singapore | ✅ | ✅ |

**Cumulative:** GPT-4o-mini **0/6** · Haiku **6/6** · Sonnet **3/6**

> The semantic layer did not change *who* got the right answer.
> Sonnet alternates wrong/right/wrong in Condition A — the year filter is a coin flip.
> But the tool call traces reveal something more important.

---

## GPT-4o-mini — Behavioral Profile (0/6 correct)

| | Cond A R1 | Cond A R2 | Cond A R3 | Cond B R1 | Cond B R2 | Cond B R3 |
|---|---|---|---|---|---|---|
| **Tool calls** | 6 | 7 | 6 | 10 | 8 | 10 |
| **Merge step** | ✅ | ❌ skipped | ✅ partial* | ✅ | ❌ skipped | ✅ |
| **Leakage** | — | — | — | ✅ | ❌ | ✅ hybrid† |
| **Year filter** | None | None | None | None | Migration | None |
| **Answer** | China (1964) | Kuwait (1991) | UAE (2007) | UAE (2007) | UAE (2023) | inconclusive |

*Run 3A: called `merge_sources()` then queried GDP from `WORLD_BANK_GDP` directly, not from merged product.  
†Run 3B: tried `'net_migration_rate_per_Kpop'` — a hallucinated hybrid (business name pattern + raw suffix).

**Year filter never applied.** Merge discipline is inconsistent.
Leakage is probabilistic — and Run 3 introduced a new variant: a hallucinated column name
that is neither the semantic business name nor the correct raw name.

---

## Haiku — Behavioral Profile (6/6 correct)

| | Cond A R1 | Cond A R2 | Cond A R3 | Cond B R1 | Cond B R2 | Cond B R3 |
|---|---|---|---|---|---|---|
| **Tool calls** | 8 | 8 | 6 | 9 | 7 | 7 |
| **Merge step** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Leakage** | — | — | — | ✅ 'gdp' | ✅ 'gdp' | ❌ none |
| **Year filter** | Round 2 | Round 2 | Direct | Round 2 | Direct | Direct |
| **Answer** | ✅ Canada | ✅ Canada | ✅ Canada | ✅ Canada | ✅ Canada | ✅ Canada |

**Only model with a perfect record — 6/6 across all conditions and runs.**

**Consistent strategy:** always merges, always applies `year=2023`, always gets Canada.
Efficiency improving — Condition A Run 3 is down to 6 calls (applied year directly, no exploratory round).

**Leakage trending down in Condition B** — present in Runs 1 and 2, absent in Run 3.
When leakage occurs, Haiku recovers via the error message and still gets the right answer.
The semantic layer would eliminate the recovery cost entirely.

---

## Sonnet — Behavioral Profile (3/6 correct)

| | Cond A R1 | Cond A R2 | Cond A R3 | Cond B R1 | Cond B R2 | Cond B R3 |
|---|---|---|---|---|---|---|
| **Tool calls** | 6 | 8 | 6 | 7 | 9 | 9 |
| **Merge step** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Leakage** | — | — | — | ❌ none | ❌ none | ❌ none |
| **Round 2 (year)** | ❌ stopped | ✅ year=2023 | ❌ stopped | ❌ stopped | ✅ year=2023 | ✅ year=2023 |
| **Answer** | ❌ Singapore | ✅ Canada | ❌ USA | ❌ Singapore | ✅ Canada | ✅ Canada |

**Year filter is the decisive probabilistic variable — nothing else changes.**

Condition A pattern: wrong / right / wrong — alternating.
Condition B pattern: wrong / right / right — tentative improvement (2/3 vs 1/3).

**No semantic leakage in Condition B across all 3 runs** — Sonnet always calls `list_columns()`
and picks the correct raw column names on the first attempt. Most disciplined discovery of the three models.

Run 3A wrong answer was *USA* (not Singapore) — the GDP query returned only USA and China
as all-time records; Sonnet reasoned USA > China on migration without checking actual rates.

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

**Leakage is model-dependent and probabilistic across 3 runs:**

| Model | Run 1 | Run 2 | Run 3 | Pattern |
|---|---|---|---|---|
| GPT-4o-mini | ✅ | ❌ | ✅ hybrid* | Probabilistic; Run 3 hallucinated a blended name |
| Haiku | ✅ | ✅ | ❌ | Mostly consistent; trending clean |
| Sonnet | ❌ | ❌ | ❌ | Never — always uses `list_columns()` correctly |

*Run 3: tried `'net_migration_rate_per_Kpop'` — neither the semantic name nor the raw column name.
A hallucinated hybrid: business name prefix + raw column suffix. Failed; recovered correctly.

**Sonnet never shows leakage** — calls `list_columns()` and picks correctly all 3 runs.

---

## The Discovery Tax (averaged across 3 runs)

Extra tool calls imposed by removing the semantic layer:

| Model | Cond A avg | Cond B avg | Extra calls | Pattern |
|---|---|---|---|---|
| GPT-4o-mini | 6.3 | 9.3 | **+3.0** | Persistent — leakage and merge failures add up |
| Haiku | 7.3 | 7.7 | **+0.4** | Near zero — fast recovery masks leakage cost |
| Sonnet | 6.7 | 8.3 | **+1.7** | `list_columns()` + second query round |

**The tax is persistent across 3 runs for every model.**

GPT-4o-mini carries the largest overhead — consistently 3+ extra calls in Condition B,
driven by leakage failures and occasional merge-skip.

Haiku averages near zero because it recovers from leakage quickly and its Condition B
strategy (7 calls) is nearly as efficient as Condition A (7.3 calls).

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
| Wrong column name (leakage) | Yes — GPT-4o-mini and Haiku intermittent | **Yes — by alignment** |
| Hallucinated column name | Yes — GPT-4o-mini Run 3B only | **Yes — by alignment** |
| No year filter | Yes — Sonnet and GPT-4o-mini intermittent | **No** |
| Partial/skipped merge | Yes — GPT-4o-mini intermittent | **No** |
| Inconclusive reasoning | Yes — GPT-4o-mini Run 3B | **Partially** |

---

## Hypothesis Verdict (3 runs)

> *"LLM agents reason more accurately and consistently through semantic business names
> than through raw technical column names."*

**The hypothesis is not confirmed.**

| | Condition A (semantic) | Condition B (raw) |
|---|---|---|
| GPT-4o-mini | 0/3 | 0/3 |
| Haiku | 3/3 | 3/3 |
| Sonnet | 1/3 | 2/3 |
| **Total** | **4/9** | **5/9** |

Condition B — *without* the semantic layer — produced more correct answers.
Sonnet did better without it. The data does not support the hypothesis.

| Claim | Verdict |
|---|---|
| **Correctness** | Not confirmed. Condition B marginally better (5/9 vs 4/9). Naming is not the driver. |
| **Efficiency** | ✅ Confirmed — Condition B costs 0.4–3.0 extra calls per model (persistent). |
| **Alignment** | ✅ Confirmed — leakage and hallucinated names prove models expect business names. |
| **Failure isolation** | ✅ Confirmed — year filter and merge discipline determine correctness, not naming. |

> **The semantic layer is proven useful — not proven necessary.**
> It closes the naming gap. It cannot close the reasoning gap.

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

## Summary (3 runs)

```
Experiment 2:  Do LLMs need a semantic layer?
Same question · Same data · Same three models · 3 runs
Two conditions: with and without the semantic layer

Finding 1:  Correctness — GPT-4o-mini 0/6, Haiku 6/6, Sonnet 3/6.
            Naming did not determine who got the right answer.

Finding 2:  Discovery tax is persistent — Condition B costs every model
            more calls: GPT-4o-mini +3.0, Haiku +0.4, Sonnet +1.7 avg.

Finding 3:  Semantic leakage is model-dependent.
            Haiku: mostly consistent. GPT-4o-mini: probabilistic + hallucinated
            hybrid name in Run 3B. Sonnet: never across all 6 Condition B runs.

Finding 4:  Core failure modes — year filter (GPT-4o-mini always, Sonnet
            intermittent) and merge discipline (GPT-4o-mini intermittent) —
            all naming-independent, all probabilistic.

Finding 5:  Sonnet Condition B trending better (2/3) vs Condition A (1/3).
            Tentative signal: raw names may prompt more methodical querying.

Verdict:    Hypothesis not confirmed. Condition B produced more correct answers
            (5/9 vs 4/9). The semantic layer is proven useful — not necessary.
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
