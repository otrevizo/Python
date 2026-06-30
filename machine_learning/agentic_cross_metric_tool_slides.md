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

## Results — At a Glance

| | Condition A (cross-metric + semantic) | Condition B (cross-metric + raw names) |
|---|---|---|
| **GPT-4o-mini** | ✅ Canada, 11.039 (2023) | ❌ Saudi Arabia, 30.367 (2022) |
| **Haiku** | ✅ Canada, 11.039 (2023) | ✅ Canada, 11.039 (2023) |
| **Sonnet** | ✅ Canada, 11.039 (2023) | ✅ Canada, 11.039 (2023) |

**Condition A: 3/3 correct — perfect.**
**Condition B: 2/3 correct — GPT-4o-mini chose year=2022.**

---

## The Complete 2×2 Matrix

| | Semantic layer | No semantic layer |
|---|---|---|
| **No cross-metric tool (Exp 2)** | 4/9 correct | 5/9 correct |
| **Cross-metric tool (Exp 3)** | **3/3 correct** | **2/3 correct** |

**Reading the matrix:**

- Adding the cross-metric tool improved both columns (4/9→3/3, 5/9→2/3)
- The semantic layer made no difference without the governed tool (Exp 2: 4 vs 5)
- The semantic layer made a decisive difference with the governed tool (Exp 3: 3/3 vs 2/3)
- **Both components together produce perfect results — neither alone is sufficient**

---

## Condition A — Behavioral Profile (3/3 correct)

All three models followed an identical 5-step strategy:

```
-> list_available_sources({})
-> load_source({'source_name': 'UN_WPP'})
-> load_source({'source_name': 'WORLD_BANK_GDP'})
-> merge_sources({...})
-> query_cross_metric({
       'filter_metric': 'gdp',
       'filter_top_n': 20,
       'rank_metric': 'net_migration_rate',
       'year': 2023          ← correct, first try, no prompting
   })
```

5 tool calls. 1 cross-metric call. `year=2023` on the first attempt.
No second round. No recovery. No divergence.

**This is the cleanest result in the entire experiment series.**
The first time GPT-4o-mini has been correct.

---

## Condition B — Behavioral Profile (2/3 correct)

| | GPT-4o-mini | Haiku | Sonnet |
|---|---|---|---|
| **Tool calls** | 6 | 7 | 7 |
| **list_columns** | ✅ | ✅ | ✅ |
| **Column selection** | GDP_USD / NetMigrationRate_per_Kpop ✅ | same ✅ | same ✅ |
| **First year tried** | **2022** ❌ | 2024 (no data) | 2024 (no data) |
| **Second year tried** | — stopped | **2023** ✅ | **2023** ✅ |
| **Answer** | ❌ Saudi Arabia (2022) | ✅ Canada (2023) | ✅ Canada (2023) |

**No semantic leakage** — all three models chose raw column names correctly on the first try.

**The failure is purely year selection:**
- Haiku and Sonnet tried 2024 → got empty result → recovered to 2023 ✅
- GPT-4o-mini tried 2022 → got valid (but wrong-year) result → stopped ❌

---

## The Year Anchoring Finding

Making `year` required eliminated the "no year filter" failure.
But it exposed a subtler question: **which year does the model choose?**

| | Condition A | Condition B |
|---|---|---|
| **GPT-4o-mini** | 2023 ✅ (first try) | 2022 ❌ (valid data, wrong year, stopped) |
| **Haiku** | 2023 ✅ (first try) | 2024 → 2023 ✅ (empty triggered recovery) |
| **Sonnet** | 2023 ✅ (first try) | 2024 → 2023 ✅ (empty triggered recovery) |

**Why did Condition A anchor to 2023 immediately?**

Semantic business names — `'net_migration_rate'`, `'gdp'` — carry associations with
current, canonical data. They implicitly signal "use the most recent complete year."
Raw column names (`GDP_USD`, `NetMigrationRate_per_Kpop`) provide no such signal —
they are technical identifiers without temporal context.

**The semantic layer provides implicit temporal anchoring**, not just naming convenience.

---

## Hypothesis Verdict

> **"A governed cross-metric tool with `year` as a required parameter will
> eliminate the year-filter failure and produce consistent correct answers
> across all models."**

**Partially confirmed.**

| Condition | Result | Reason |
|---|---|---|
| Cross-metric + semantic (Cond A) | ✅ **Confirmed — 3/3** | Tool + naming together anchor year correctly |
| Cross-metric + raw names (Cond B) | ❌ Not confirmed — 2/3 | Year required, but GPT-4o-mini chose 2022 |

`year` required is necessary but not sufficient.
The semantic layer determines whether the model chooses the *right* year on the first try.

---

## Revision to Experiment 2

Experiment 2 concluded: *"The semantic layer is proven useful — not proven necessary."*

**That conclusion was conditional on a poorly structured tool.**

| Condition | Correctness | What changed |
|---|---|---|
| Exp 2: no tool, no semantic | 5/9 | Baseline |
| Exp 2: no tool, semantic | 4/9 | Semantic layer alone: no help |
| Exp 3: governed tool, no semantic | 2/3 ≈ 6/9 | Tool alone: major improvement |
| Exp 3: governed tool + semantic | **3/3 ≈ 9/9** | Both together: perfect |

**The semantic layer IS necessary — but only when the tool is also governed.**

With a poor tool, naming makes no difference.
With a governed tool, naming becomes the decisive variable.

---

## The Interaction Is Superadditive

Neither component alone achieves perfect results:

```
Semantic layer alone:   4/9  (Exp 2A) — no improvement over baseline
Governed tool alone:    2/3  (Exp 3B) — large improvement, not complete
Both together:          3/3  (Exp 3A) — perfect

Neither:                5/9  (Exp 2B) — baseline
```

**The combination produces results that neither achieves separately.**

This is the core neurosymbolic claim made concrete:

```
SYMBOLIC STRUCTURE = governed tool + semantic layer

  Governed tool     → enforces what must be computed (cross-metric join)
  Semantic layer    → anchors how the model reasons (year, naming, context)
  Required year     → enforces that a year is specified
  Semantic names    → guide the model to specify the right year

Neither is reducible to the other.
Both are necessary for consistent, correct results across all models.
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

## Summary

```
Experiment 3:  Does a governed cross-metric tool fix the reasoning gap?

Design:        2×2 matrix completing Experiments 1–2
               Cross-metric tool × semantic layer (both conditions)
               year required by schema in both conditions

Finding 1:     Condition A (tool + semantic): 3/3 correct — perfect.
               First time GPT-4o-mini correct in the entire series.

Finding 2:     Condition B (tool + raw names): 2/3 correct.
               Year required, but GPT-4o-mini chose 2022 instead of 2023.

Finding 3:     Semantic layer provides implicit temporal anchoring.
               All Cond A models chose year=2023 on the first try.
               Cond B models guessed (2024 or 2022) and needed recovery.

Finding 4:     The interaction is superadditive.
               Neither governed tool nor semantic layer alone is sufficient.
               Both together produce perfect results across all models.

Revision:      Experiment 2 conclusion ("useful but not necessary") was
               conditional on a poorly structured tool. With a governed tool,
               the semantic layer IS necessary.
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
