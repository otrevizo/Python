# `data_product_lib` — Tutorial & Reference

Personal documentation, written the way pandas documents itself: a short
tutorial (this file) plus the introspection habit (`?`, `??`, `help()`) for
everything this file doesn't cover. Grounded directly in the three vignette
notebooks, not the original design spec, so this reflects what was actually built.

Notebooks in `python_vignettes/data_products/`:

| Notebook | What it covers |
|---|---|
| `data_product_lib_vignette.ipynb` | Every class in isolation on synthetic data. Start here. |
| `un_wpp_data_product.ipynb` | Single-source: UN WPP → DP1 |
| `un_wpp_wb_data_product.ipynb` | Composition: DP1 (UN WPP) ⊕ DP2 (World Bank) → DP3 |

Module location: `python_vignettes/data_products/data_product_lib.py`

---

## Origin — what this module is and is not

`data_product_lib` is a **custom module written for this project**, not a
published package. It does not exist on PyPI, has no external GitHub, and has
no maintainer other than the owner of this repo. The import works because
Jupyter's working directory is `python_vignettes/data_products/`, where the
`.py` file lives alongside the notebooks.

To confirm where Python found it:

```python
import data_product_lib
print(data_product_lib.__file__)
# ~/GitHub/Python/python_vignettes/data_products/data_product_lib.py
```

**Where the ideas come from:**
The four classes implement a small, opinionated subset of the *data product*
concept from the data mesh literature. The intellectual lineage:

| Class | Concept source |
|---|---|
| `DataProductMetadata` | Data mesh — Zhamak Dehghani, *Data Mesh* (O'Reilly, 2022): a data product must be discoverable, addressable, and owned |
| `SemanticLayer` | BI semantic layers (Looker/LookML, dbt metrics layer): decouple business vocabulary from physical column names |
| `LineageTracker` | Data lineage tools (OpenLineage, DataHub, Apache Atlas): append-only audit trail of every transformation |
| `DataProduct` | Data contracts (Chad Sanderson, `datacontract.com`): schema + quality + lineage bundled with the data as a single governed artifact |

The module was built from scratch in June 2026 to demonstrate these concepts
in a self-contained, dependency-free way. The only external libraries it uses
are `pandas` (already in the environment) and Python's `json` / `dataclasses`
stdlib modules.

**If you want production-grade equivalents:**
- Lineage at scale: OpenLineage (`openlineage.io`), DataHub (`datahubproject.io`)
- Semantic layer at scale: dbt Semantic Layer (`docs.getdbt.com`), Looker
- Data contracts spec: `datacontract.com`
- Schema standards: Frictionless Data (`specs.frictionlessdata.io/table-schema`)

---

## Where pandas keeps its docs (for comparison)

- User Guide (worked examples by topic): https://pandas.pydata.org/docs/user_guide/index.html
- API reference (auto-built from docstrings): https://pandas.pydata.org/docs/reference/index.html

Both are generated from the docstrings living in pandas's source code by a
tool called Sphinx. `DataProduct?` in a notebook reads from the same kind of
source, just rendered inline instead of as a website. If `data_product_lib`
ever grows into something worth a real doc site, good docstrings now are
what make that possible later.

---

## Quickstart

```python
from data_product_lib import (
    DataProductMetadata,
    SemanticLayer,
    LineageTracker,
    DataProduct,
)
from datetime import datetime, timezone

# 1. Metadata — who owns it, where it came from
metadata = DataProductMetadata(
    name='My Product', description='...', domain='...', owner='...',
    source='...', source_url='...', license='...', version='1.0',
    refresh_frequency='...', created_at=datetime.now(timezone.utc).isoformat(),
)

# 2. Semantic layer — business-friendly aliases for raw columns
semantic = SemanticLayer()
semantic.register('business_name', 'raw_column', 'unit', 'description')

# 3. Lineage — log each pipeline step right after it runs
lineage = LineageTracker()
lineage.log('1-load', 'load_source', (0, 0), df.shape, notes='optional note')

# 4. Assemble — note all four args are positional, in this order
dp = DataProduct(df, metadata, semantic, lineage)

# 5. Inspect
dp.schema()                                      # {column: dtype}
dp.quality()                                     # {row_count, completeness_pct, freshness}
dp.card()                                        # pretty-printed summary
dp.contract('output/my_product_contract.json')   # JSON sidecar
```

---

## 1. `DataProductMetadata`

A plain dataclass. Answers: *who owns this, where did it come from, is it
safe to use?*

| Field | Type | Purpose |
|---|---|---|
| `name` | str | Short identifier for the product |
| `description` | str | One-sentence summary |
| `domain` | str | Business domain (e.g. Sales, Demographics) |
| `owner` | str | Person or team responsible |
| `source` | str | Human-readable source name |
| `source_url` | str | Canonical URL for the source |
| `license` | str | Data licence (e.g. CC BY 4.0, proprietary) |
| `version` | str | Semantic version of this product |
| `refresh_frequency` | str | How often the data is updated |
| `created_at` | str | ISO-8601 timestamp of when this product was built |

All fields are required, all are strings — note that `created_at` is a
string you generate yourself (`datetime.now(timezone.utc).isoformat()`),
not something the class fills in automatically.

Real example, from the UN WPP vignette:

```python
metadata = DataProductMetadata(
    name              = 'UN WPP Net Migration',
    description       = 'Country-year panel of UN WPP 2024 demographic indicators, 1961–2023',
    domain            = 'Demographics',
    owner             = 'Oscar Trevizo',
    source            = 'UN World Population Prospects 2024',
    source_url        = 'https://population.un.org/wpp/',
    license           = 'CC BY 3.0 IGO',
    version           = '1.0',
    refresh_frequency = 'Every 2 years (UN WPP release cycle)',
    created_at        = datetime.now(timezone.utc).isoformat(),
)
```

---

## 2. `SemanticLayer`

A registry mapping a **business name** (stable) to the underlying **column
name** (may change between source versions), its unit, and a description.

Why it matters: code that references `net_migration_rate` instead of
`NetMigrationRate_per_Kpop` keeps working even if a future WPP release
renames the column.

| Method | Signature | What it does |
|---|---|---|
| `.register()` | `(name, column, unit, description, source_system=None)` | Add one entry |
| `.get()` | `(name) → dict` | Look up one entry by business name |
| `.to_dict()` | `() → dict` | Return the full registry as a plain dict |

```python
semantic = SemanticLayer()
semantic.register('net_migration_rate', 'NetMigrationRate_per_Kpop',
                   'per 1,000 population', 'Net migrants per 1,000 residents, UN WPP')

entry = semantic.get('net_migration_rate')
# {'column': 'NetMigrationRate_per_Kpop', 'unit': 'per 1,000 population',
#  'description': 'Net migrants per 1,000 residents, UN WPP', 'source_system': None}

col = entry['column']      # resolves to the real column name
df[[col]].describe()       # use it without hard-coding the raw name
```

`.to_dict()` returns `{business_name: {column, unit, description,
source_system}}`, which is convenient to drop straight into a DataFrame.

In a single-source product, `source_system` is often left `None`. In a
multi-source merged product it distinguishes provenance — each entry carries
the name of the source it came from:

```python
wpp_semantic.register('net_migration_rate', 'NetMigrationRate_per_Kpop',
                       'per 1,000 population', 'Net migrants per 1,000 residents',
                       source_system='UN WPP 2024')

wb_semantic.register('gdp_growth', 'GDP_growth_pct', '% per year',
                      'GDP growth rate (NY.GDP.MKTP.KD.ZG)',
                      source_system='World Bank WDI')
```

The merged product's `.card()` then shows which business name came from which
source — useful when debugging a join or auditing a contract.

`.to_dict()` as a DataFrame:

```python
import pandas as pd
pd.DataFrame(semantic.to_dict()).T.rename_axis('business_name')
```

---

## 3. `LineageTracker`

An append-only log. Each `.log()` call records one pipeline step: its input
shape, output shape, the operation name, optional notes, and a UTC
timestamp it generates for you.

| Method | Signature | What it does |
|---|---|---|
| `.log()` | `(step, operation, input_shape, output_shape, notes=None)` | Append one entry |
| `.to_list()` | `() → list[dict]` | Return all entries as a list of dicts |

```python
lineage = LineageTracker()

lineage.log(
    step         = '1-load',
    operation    = 'load_un_wpp',
    input_shape  = (0, 0),
    output_shape = raw.shape,
    notes        = 'Estimates sheet, skiprows=16',
)
lineage.log(
    step         = '2-filter',
    operation    = 'filter_countries',
    input_shape  = raw.shape,
    output_shape = filtered.shape,
    notes        = "LocType == 'Country'",
)

pd.DataFrame(lineage.to_list())
```

`step` is just a label you choose (`'1-load'`, `'2-filter'`); the class
doesn't enforce numbering or order, it just records what you tell it, in the
order you tell it.

---

## 4. `DataProduct`

The top-level class. Assembles a DataFrame plus the three objects above into
one governed artifact.

**Constructor:** `DataProduct(data, metadata, semantic_layer=None, lineage=None)` —
`data` and `metadata` are required; `semantic_layer` and `lineage` are optional
(the class creates empty instances for you if omitted). Attributes after
construction: `dp.data`, `dp.metadata`, `dp.semantic_layer`, `dp.lineage`.

| Method | Returns / does |
|---|---|
| `.schema()` | `{column: dtype}` for every column |
| `.quality()` | `{row_count, column_count, completeness_pct: {col: pct}, freshness}` |
| `.card()` | Prints a formatted summary: metadata + semantic layer + quality + lineage |
| `.contract(path)` | Writes everything above to a JSON sidecar file |

```python
dp = DataProduct(filtered_df, metadata, semantic, lineage)

dp.schema()
# {'region': 'object', 'product': 'object', 'year': 'int64', ...}

dp.quality()
# {'row_count': 21, 'column_count': 5, 'completeness_pct': {'region': 100.0, ...}, 'freshness': '...'}

dp.card()
```

`.card()` output looks like this (from the synthetic tutorial example):

```
==============================================================
  Data Product : Store Sales Demo
==============================================================
  Description  : Synthetic store-sales data for data_product_lib tutorial
  Domain       : Sales
  Owner        : Oscar Trevizo
  ...
  Semantic layer (3 entries):
    revenue                        → revenue_usd  [USD]
    units                          → units_sold  [count]
    sales_year                     → year  [year]
==============================================================
  All columns 100% complete.
==============================================================
  Lineage (2 steps):
    [1-load] generate_synthetic  (0, 0) → (30, 5)  // np.random.default_rng(seed=42), n=30
    [2-filter] year_filter  (30, 5) → (21, 5)  // year >= 2023
==============================================================
```

`.contract(path)` writes a JSON file with top-level keys `['metadata',
'schema', 'semantic_layer', 'quality', 'lineage']`, the same information as
`.card()` but machine-readable, sitting next to the data file it describes:

```python
import os
os.makedirs('output', exist_ok=True)
dp.data.to_parquet('output/my_product.parquet', index=False)
dp.contract('output/my_product_contract.json')
```

---

## 5. Data Product Composition (DP1 ⊕ DP2 → DP3)

`data_product_lib` has no built-in merge method — composition is a pattern,
not a class. The pattern from `un_wpp_wb_data_product.ipynb`:

```python
def merge_data_products(dp1, dp2, on):
    """Inner join two DataProducts; combine semantic layers; inherit lineage."""
    merged_df = pd.merge(dp1.data, dp2.data, on=on, how='inner')

    # Combined semantic layer — source_system distinguishes which source each
    # business name came from
    merged_semantic = SemanticLayer()
    for name, entry in dp1.semantic_layer.to_dict().items():
        merged_semantic.register(name, entry['column'], entry['unit'],
                                 entry['description'], entry['source_system'])
    for name, entry in dp2.semantic_layer.to_dict().items():
        merged_semantic.register(name, entry['column'], entry['unit'],
                                 entry['description'], entry['source_system'])

    # Full lineage from both parents, prefixed, then the merge step appended
    merged_lineage = LineageTracker()
    for s in dp1.lineage.to_list():
        merged_lineage.log(f"dp1/{s['step']}", s['operation'],
                           s['input_shape'], s['output_shape'], s['notes'])
    for s in dp2.lineage.to_list():
        merged_lineage.log(f"dp2/{s['step']}", s['operation'],
                           s['input_shape'], s['output_shape'], s['notes'])
    merged_lineage.log('merge', 'inner_join', dp1.data.shape, merged_df.shape,
                       f'keys: {"+".join(on)}  |  DP2 input: {dp2.data.shape}')

    return merged_df, merged_semantic, merged_lineage
```

Then assemble DP3:

```python
merged_df, merged_semantic, merged_lineage = merge_data_products(
    dp_wpp, dp_wb, on=['ISO3', 'Year']
)

merged_metadata = DataProductMetadata(
    name    = 'UN WPP + World Bank — Demographics and GDP',
    source  = 'UN WPP 2024 + World Bank WDI',
    license = 'CC BY 3.0 IGO (WPP) + CC BY 4.0 (WB)',
    # ... other fields
)

dp_merged = DataProduct(merged_df, merged_metadata, merged_semantic, merged_lineage)
dp_merged.card()   # lineage shows all 5 steps: 3 WPP + 1 WB + 1 merge
```

**Known tradeoff — semantic name collisions:**
The merge loop registers DP1's entries then DP2's into one dict keyed by
business name. Without a guard, a name present in both sources would silently
overwrite DP1's definition with DP2's. The function handles this with a
pre-merge collision check that raises `ValueError` immediately rather than
proceeding with a shadowed entry:

```python
collisions = set(dp1.semantic_layer.to_dict()) & set(dp2.semantic_layer.to_dict())
if collisions:
    raise ValueError(f'Semantic name collision(s): {sorted(collisions)}')
```

This didn't fire for WPP ⊕ WB (zero overlap between `net_migration_rate`,
`population`, … and `gdp`, `gdp_growth`) but will matter the moment a third
source also registers `population`.

**Why join on ISO3, not country name?**
UN WPP and World Bank sometimes spell country names differently
(e.g. "Bolivia" vs "Bolivia (Plurinational State of)"). ISO3 is the stable,
unambiguous join key — it's in both sources and never varies.

**What the merged `.card()` shows differently:**
- Lineage has `dp1/1-load`, `dp1/2-filter`, … then `dp2/1-load`, … then `merge`
- Semantic layer lists all 7 entries (5 WPP + 2 WB) with their `source_system`
- Quality reports completeness across all columns from both sources

**Cross-source query without hard-coding column names:**

```python
mig_col = dp_merged.semantic_layer.get('net_migration_rate')['column']  # UN WPP
gdp_col = dp_merged.semantic_layer.get('gdp_growth')['column']           # World Bank

top10 = (dp_merged.data[['Location', 'Year', mig_col, gdp_col]]
         .query('Year == 2020')
         .nlargest(10, mig_col))
```

If either source renames its column, only the `register()` call changes —
the query above keeps working unchanged.

---

## Three worked examples in this repo

| Notebook | What it shows |
|---|---|
| `data_product_lib_vignette.ipynb` | Every class in isolation, on a 30-row synthetic store-sales table. Start here. |
| `un_wpp_data_product.ipynb` | Single-source: `load_un_wpp()` → `filter_countries()` → `clean_types()`, wrapped into DP1, exported to parquet + JSON contract. |
| `un_wpp_wb_data_product.ipynb` | Composition: DP1 (UN WPP, 5 indicators) ⊕ DP2 (World Bank GDP, 2 indicators) → DP3 via inner join on ISO3 + Year; 5-step inherited lineage; cross-source semantic query. |

---

## Introspection in JupyterLab

Same habit works on this module as on pandas, since both are just reading
docstrings:

| Command | What it shows |
|---|---|
| `DataProduct?` | Signature + docstring + file path |
| `DataProduct??` | All of the above, plus the actual source code |
| `help(DataProduct)` | Plain-Python equivalent; works outside Jupyter too |
| `DataProduct.card?` | Docstring for one method only |
| `Shift+Tab` (cursor inside parens) | Same docstring, popped up inline |

---

## Further reading

`data_product_lib` implements a small subset of ideas from the data mesh and
data contract literature. Loosely, in terms of this module:

- **`DataProductMetadata`** maps to data mesh's idea of a data product as a
  discoverable, addressable unit with an owner and a contract, not just a
  table sitting in a database.
- **`SemanticLayer`** is a minimal version of what tools like dbt's metrics
  layer or a BI semantic layer do at scale: decouple the name people use
  from the column name that happens to exist today.
- **`LineageTracker`** is a toy version of what production lineage tools
  (OpenLineage, DataHub) track automatically across an entire pipeline.

| Concept | Where to read more |
|---|---|
| Data products & data mesh | Zhamak Dehghani — *Data Mesh* (O'Reilly, 2022); Martin Fowler's summary at `martinfowler.com/articles/data-mesh-principles.html` |
| Data contracts | Chad Sanderson's blog (`dataproducts.substack.com`); open spec at `datacontract.com` |
| Semantic / metrics layers | dbt Semantic Layer docs (`docs.getdbt.com`); Looker/LookML semantic layer pattern |
| Frictionless Data Table Schema | Lightweight open standard for column schemas: `specs.frictionlessdata.io/table-schema` |
| Lineage tools (production-grade) | OpenLineage (`openlineage.io`); Apache Atlas; DataHub (`datahubproject.io`) |

> URLs above came from the notebook as written by Claude Code, from training
> knowledge rather than a live fetch. Worth a quick check before citing them
> anywhere, same caution as any AI-suggested reference.
