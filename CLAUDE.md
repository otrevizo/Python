# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- **Python 3.14.3** in a virtual environment named `myenv` on macOS (Apple Silicon M5)
- **Primary IDE**: JupyterLab — almost all work lives in `.ipynb` notebooks
- The active environment is activated with `source myenv/bin/activate`

## Setup

```bash
# Create and activate the virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Core dependencies
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels pmdarima scipy
pip install openai anthropic jupyterlab yfinance sqlalchemy

# Launch JupyterLab
jupyter lab
```

**API keys** are loaded from the shell environment, never hardcoded:
```bash
export ANTHROPIC_API_KEY='sk-ant-...'   # add to ~/.zshrc
```

## Repository Structure

| Folder | Contents |
|---|---|
| `python_vignettes/` | Language fundamentals, pandas, numpy, plotting, stats, OOP, R-to-Python (`_r2p` suffix) conversions |
| `machine_learning/` | Supervised learning notebooks following ISLR chapters (Ch3, Ch4, Ch8, Ch10); Kaggle examples; LLM hello world; agentic AI vignette |
| `toolbox/` | Reusable standalone notebooks: descriptive stats, prediction metrics, visualization helpers |
| `use_cases/` | End-to-end applied analyses on public datasets (migration, FIFA, markets) |
| `data/` | CSV/XLS/SQLite datasets used across notebooks |

## Notebook Conventions

Every notebook opens with a module-level docstring (Cell [1]) that includes:
- `@author`, `@institution`, `@environment`, description, and revision history
- A structured `Revision History:` block with dates and bullet points

### `.py` companion files
Some notebooks have a paired `.py` file (e.g. `python_functions_vignette.py` alongside `.ipynb`). The `python_vignettes/` folder also has importable modules:
- `my_stats_ftns_module.py` — hand-rolled `mean_s()` / `stdev_s()` using only Python built-ins
- `functions_vignette_library.py` — function-pattern library imported by `python_functions_vignette.ipynb`
- `my_stats_ftns_calls.py` — caller script for the stats module

## Naming Conventions

- `_r2p` suffix — notebooks that are direct R-to-Python translations
- `_vignette` suffix — focused demonstrations of a single concept or library
- `_oo` suffix — object-oriented implementations
- `_ISLR_ChN` — tied to a specific chapter of *Introduction to Statistical Learning with Python*

## Agentic AI Pattern (`machine_learning/agentic_ai_vignette_yfinance.ipynb`)

The agent loop pattern used here:
1. Define Python tool functions (`get_stock_price`, `get_portfolio_summary` backed by `yfinance`)
2. Register JSON tool schemas with Claude
3. Loop: send message → receive `tool_use` → execute Python function → feed result back → repeat until `end_turn`

Uses `claude-haiku-4-5-20251001` for speed/cost. The dispatch table (`TOOL_FUNCTIONS`) maps tool names to callables.

## Git Workflow

```bash
git add <file>
git commit -m "Descriptive message"
git push
```

See `git_cheatsheet.md` for PAT renewal and full reference.
