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

# Does a Governed Cross-Metric Tool Fix the Reasoning Gap?

### Experiment 3 — Cross-Metric Tool + Semantic Layer

Oscar Trevizo
Harvard Extension School — Graduate Certificate in Data Science (2023)
Independent project · `machine_learning/agentic_cross_metric_tool.ipynb`

---

## The Progression

| Experiment | Question | Key finding |
|---|---|---|
| **Exp 1** | Do models diverge on cross-metric reasoning? | Yes — 0/3, 2/3, 3/3 correct across models |
| **Exp 2** | Does the semantic layer fix it? | No — "useful but not necessary" (4/9 vs 5/9) |
| **Exp 3** | Does a governed cross-metric tool fix it? | **This experiment** |

**The structural gap (Experiments 1 and 2):**

No tool returned *"migration rate filtered to the top-20 GDP countries."*
Models had to query two separate result sets and reason across them.
The year filter — whether to anchor to 2023 — was a probabilistic neural choice.

**The intervention:**

```python
query_cross_metric(
    filter_metric='gdp',            # which metric defines the filter set
    filter_top_n=20,                # how many countries to keep
    rank_metric='net_migration_rate', # which metric to rank by within that set
    year=2023                       # REQUIRED — schema enforces it
)
```

---

## The 2×2 Design

| | Semantic layer | No semantic layer |
|---|---|---|
| **No cross-metric tool** | Exp 2 Cond A · 4/9 correct | Exp 2 Cond B · 5/9 correct |
| **Cross-metric tool** | **Exp 3 Cond A** | **Exp 3 Cond B** |

Experiment 3 fills the bottom row.

**What each comparison isolates:**

- **Row comparison:** Effect of the cross-metric tool (within each naming condition)
- **Column comparison:** Effect of the semantic layer (within each tool condition)
- **Diagonal:** Combined effect — governed tool + semantic layer vs neither

`year` is a **required** schema parameter in both Exp 3 conditions.
The model cannot call the tool without specifying a year.

---

## Results — At a Glance (2 runs)

| | Cond A Run 1 | Cond A Run 2 | Cond B Run 1 | Cond B Run 2 |
|---|---|---|---|---|
| **GPT-4o-mini** | ❌ (2022) | ❌ (2022) | ❌ (2022) | ✅ (2023) |
| **Haiku** | ✅ (2023) | ✅ (2023) | ✅ (2023) | ✅ (2023) |
| **Sonnet** | ✅ (2023) | ✅ (2023) | ✅ (2023) | ✅ (2023) |

**Condition A: 5/6 correct · Condition B: 5/6 correct**

Run 1 showed Cond A 3/3, Cond B 2/3.
Run 2 reversed it: Cond A 2/3, Cond B 3/3.
After 2 runs, both conditions are equal. The tool structure is the primary driver.

---

## The Complete 2×2 Matrix (2 runs)

| | Semantic layer | No semantic layer |
|---|---|---|
| **No cross-metric tool (Exp 2)** | 4/9 correct | 5/9 correct |
| **Cross-metric tool (Exp 3, 2 runs)** | **5/6 correct** | **5/6 correct** |

**Reading the matrix:**

- Adding the cross-metric tool improved both columns substantially (4/9→5/6, 5/9→5/6)
- The semantic layer made no difference in either tool condition after 2 runs
- **The tool structure is the dominant driver — naming condition is secondary**
- The single remaining failure (GPT-4o-mini, 1/4) persists in both naming conditions

---

## Condition A — Behavioral Profile (5/6 correct)

| | Run 1 | Run 2 |
|---|---|---|
| GPT-4o-mini | ❌ year=2022 (5 calls) | ❌ year=2022 (5 calls) |
| Haiku | ✅ year=2023 direct (5 calls) | ✅ 2024→2023 (6 calls) |
| Sonnet | ✅ year=2023 direct (5 calls) | ✅ 2024→2023 (6 calls) |

**GPT-4o-mini chose year=2022 in both Condition A runs** — consistent 2022 bias with semantic names.
Gets valid data for 2022, stops, confident but wrong.

**Haiku and Sonnet are always correct** but by different paths:
- Run 1: went directly to 2023
- Run 2: tried 2024 first (empty result) → recovered to 2023

The empty-result signal from 2024 acts as a symbolic correction for the neural year guess.
Both paths work. The 2022 trap doesn't occur because these models reach for recent years (2023–2024),
not 2022.

---

## Condition B — Behavioral Profile (5/6 correct)

| | Run 1 | Run 2 |
|---|---|---|
| GPT-4o-mini | ❌ year=2022 (6 calls) | ✅ year=2023 direct (6 calls) |
| Haiku | ✅ 2024→2023 (7 calls) | ✅ year=2023 direct (6 calls) |
| Sonnet | ✅ 2024→2023 (7 calls) | ✅ year=2023 direct (6 calls) |

**No semantic leakage in either run** — all models chose raw column names correctly on the first try.

**Run 2 Condition B is the cleanest result of the experiment:** all three models went directly to
`year=2023` without needing a recovery round. 6 tool calls each.

**GPT-4o-mini's recovery in Run 2:** chose 2023 directly — probabilistic, not structural.
The same model chose 2022 in Run 1. No consistent pattern explains the difference.

**The failure mode unique to GPT-4o-mini:** When it picks a year with valid data (2022),
it stops. Haiku and Sonnet reach for 2023–2024; if empty, they recover. GPT-4o-mini
reaches for 2022 and finds data — no error signal, no recovery.

---

## The Year Selection Finding (revised after 2 runs)

Making `year` required eliminated "no year filter" — but exposed a new question: **which year?**

| Model | Cond A R1 | Cond A R2 | Cond B R1 | Cond B R2 | Rate |
|---|---|---|---|---|---|
| GPT-4o-mini | 2022 ❌ | 2022 ❌ | 2022 ❌ | 2023 ✅ | 1/4 |
| Haiku | 2023 ✅ | 2024→2023 ✅ | 2024→2023 ✅ | 2023 ✅ | 4/4 |
| Sonnet | 2023 ✅ | 2024→2023 ✅ | 2024→2023 ✅ | 2023 ✅ | 4/4 |

**Run 1 suggested semantic names anchor to 2023. Run 2 disproves it.**
Both conditions are 5/6 after 2 runs — naming condition doesn't determine year choice.

**GPT-4o-mini has a 2022 bias** — chose 2022 three of four times, in both naming conditions.
This is model-specific, not naming-dependent. Possibly a training data artefact
(2022 GDP/migration rankings were widely published and cited).

**The fatal pattern:** 2022 has valid data → tool succeeds → model stops → wrong answer.
Haiku/Sonnet reach for 2023–2024; if 2024 is empty, they recover. GPT-4o-mini falls into
the 2022 trap because valid data produces no error signal.

---

## Hypothesis Verdict (2 runs)

> **"A governed cross-metric tool with `year` as a required parameter will
> eliminate the year-filter failure and produce consistent correct answers
> across all models."**

**Partially confirmed — with important nuance.**

The cross-metric tool eliminated the "no year filter" failure. Year is always provided.
But `year` required is not the same as `year` correct.

| Model | Exp 3 correct rate | Remaining failure |
|---|---|---|
| GPT-4o-mini | **1/4** | 2022 bias — picks valid-but-stale year, no recovery signal |
| Haiku | **4/4** | None — reaches for recent year, recovers if empty |
| Sonnet | **4/4** | None — same recovery pattern as Haiku |

**The semantic layer does not fix GPT-4o-mini's 2022 bias** — it fails in both conditions.
After 2 runs, both naming conditions produce 5/6. The tool is the primary driver; naming is not.

---

## Revision to Experiment 2 (updated after 2 runs)

| Condition | Correctness | What changed |
|---|---|---|
| Exp 2: no tool, no semantic | 5/9 | Baseline |
| Exp 2: no tool, semantic | 4/9 | Semantic layer alone: no help |
| Exp 3: governed tool, no semantic (2 runs) | 5/6 | Tool alone: major improvement |
| Exp 3: governed tool + semantic (2 runs) | 5/6 | Same as without semantic |

**Exp 2 conclusion holds: the semantic layer is proven useful, not proven necessary.**

Run 1 appeared to show semantic layer advantage (3/3 vs 2/3).
Run 2 reversed it (2/3 vs 3/3). After 2 runs, both conditions equal.

**The tool structure is the primary intervention.** Adding the cross-metric tool
improved correctness from ~4–5/9 to 5/6 in both naming conditions.
The remaining gap — GPT-4o-mini's 2022 year bias — is not fixed by naming.

---

## What the Tool Adds — Row Comparison

**Adding the cross-metric tool (Exp 2 → Exp 3), within each naming condition:**

| Naming condition | Without tool (Exp 2) | With tool (Exp 3, 2 runs) | Improvement |
|---|---|---|---|
| Semantic layer | 4/9 (44%) | 5/6 (83%) | **+39 ppts** |
| Raw column names | 5/9 (56%) | 5/6 (83%) | **+28 ppts** |

The cross-metric tool is a large, consistent improvement in both naming conditions.

**What the semantic layer adds — column comparison (Exp 3 only):**

| Tool condition | Semantic | Raw names | Difference |
|---|---|---|---|
| Cross-metric tool (Exp 3, 2 runs) | 5/6 | 5/6 | **0** |

After 2 runs: no detectable benefit from the semantic layer when the tool is governed.

```
Primary driver:  governed cross-metric tool (+33 ppts avg)
Secondary driver: naming condition — not detectable at this sample size
Residual failure: GPT-4o-mini year bias — naming-independent, tool-independent
```

---

## What Each Component Contributes

| Component | Failure it prevents | Evidence |
|---|---|---|
| **Cross-metric tool** | Disconnected two-step reasoning | Exp 2: models queried two sets, reasoned across them |
| **Required year param** | "No year filter" omission | Exp 1/2: GPT-4o-mini never applied year; Exp 3: always does |
| **Semantic business names** | Wrong year selection | Exp 3B: GPT-4o-mini chose 2022; Exp 3A: chose 2023 correctly |
| **All three together** | All above | Exp 3A: 3/3 perfect, all models, first try |

**Each symbolic component closes a specific failure mode.**
Removing any one of them re-opens a gap.

---

## The Neurosymbolic Conclusion

```
SYMBOLIC (Deterministic)              NEURAL (Probabilistic)
─────────────────────────             ──────────────────────────
Cross-metric tool                     Which year to specify
Required year parameter               Whether to recover from empty result
Semantic business names               Column name guessing (Condition B)
Governed column resolution            Tool call ordering
```

Experiment 3 Condition A collapses nearly all neural variation into the symbolic layer.
The model's job is reduced to: load, merge, call the governed tool correctly.

**Haiku's perfect record (6/6 across Experiments 2 and 3) shows that the right
neural strategy is achievable. Experiment 3A shows that the right symbolic structure
makes it achievable for every model, including GPT-4o-mini.**

The symbolic layer cannot fully substitute for neural reasoning —
but it can constrain the space of neural choices until correct behavior
is the path of least resistance.

---

## Summary (2 runs)

```
Experiment 3:  Does a governed cross-metric tool fix the reasoning gap?

Design:        2×2 matrix · cross-metric tool × naming condition · 2 runs
               year required by schema in both conditions

Finding 1:     The cross-metric tool is the primary driver.
               Both naming conditions improved from ~44–56% to 83% correct.
               Tool structure >> naming condition.

Finding 2:     Naming condition makes no detectable difference after 2 runs.
               Cond A 5/6, Cond B 5/6 — equal. Run 1 (Cond A better) and
               Run 2 (Cond B better) cancel each other out.

Finding 3:     GPT-4o-mini has a 2022 year bias — naming-independent.
               Chose 2022 three of four times. Gets valid data, stops,
               confident but wrong. 2022 trap: no error signal, no recovery.

Finding 4:     Haiku and Sonnet recover via empty-result signal.
               Trying 2024 (no data) forces a retry at 2023. Both models
               are 4/4 across all conditions and runs.

Next:          Experiment 4 — add get_available_years() tool. If the model
               sees data ends at 2023, it cannot choose 2022 as "most recent."
               Tests whether the failure is information access or reasoning.
```

---

## References

- **Data:** UN WPP 2024 (population.un.org/wpp) · World Bank WDI (databank.worldbank.org)
- **Anthropic Tool Use:** docs.anthropic.com/en/docs/tool-use
- **OpenAI Function Calling:** platform.openai.com/docs/guides/function-calling
- **Data products:** Dehghani (2022) *Data Mesh*, O'Reilly
- **Experiment 1:** `machine_learning/agentic_model_reasoning_divergence.ipynb`
- **Experiment 2:** `machine_learning/agentic_semantic_layer_necessity.ipynb`
- **Experiment 3:** `machine_learning/agentic_cross_metric_tool.ipynb`

```
~/GitHub/Python/machine_learning/
  agentic_model_reasoning_divergence.ipynb       ← Exp 1
  agentic_model_reasoning_divergence_slides.md
  agentic_semantic_layer_necessity.ipynb         ← Exp 2
  agentic_semantic_layer_necessity_slides.md
  agentic_cross_metric_tool.ipynb                ← Exp 3
  agentic_cross_metric_tool_slides.md            ← these slides
```

*Render:* `marp agentic_cross_metric_tool_slides.md --html`
