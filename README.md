# Oscar Trevizo — Python Portfolio

Welcome! This repository contains Python projects, vignettes, and tools developed
over the course of my graduate studies at Harvard Extension School and through
independent work bridging 30 years of industry experience in telecom analytics,
R&D, and data science.

This repo is intended for students, collaborators, and anyone interested in
applied data science and machine learning with Python.

---

## Folders

| Folder | Description |
|---|---|
| `machine_learning` | Supervised learning vignettes and Kaggle examples: Linear Regression, Logistic Regression, K-NN, Naive Bayes, SVM/SVC, Time Series OO, and LLM hello world (OpenAI + Anthropic) |
| `use_cases` | Real-world applications of data science and machine learning on public datasets |
| `toolbox` | Reusable Python functions and scripts for data wrangling, visualization, and analysis |
| `python_vignettes` | Python language fundamentals, functions, and coding patterns |
| `data` | Datasets used across projects |
| `images` | Visualizations and plots related to projects |

---

## Tech Stack

| Category | Libraries / Tools |
|---|---|
| **Languages** | Python, R |
| **ML / Stats** | scikit-learn, statsmodels, pmdarima, scipy |
| **Time Series** | ARIMA, SARIMAX, VAR, seasonal decomposition |
| **AI / LLM** | anthropic, openai, langchain, faiss-cpu |
| **Data** | pandas, numpy, yfinance, SQLAlchemy |
| **Visualization** | matplotlib, seaborn |
| **Dev** | JupyterLab, Spyder, GitHub, macOS M5 |

---

## Background

- **30 years** in telecom analytics — Lucent / ALU / Nokia
- **R&D** at Tellabs, Fermilab, and DuPont
- **Graduate studies** — Harvard Extension School, Data Science Certificate (2023);
  Georgia Tech MSEE; Illinois Tech MBA
- **Undergraduate** — BSE Bioengineering (UIC), transferred from Ohio State BSEE
- **Visiting Professor** at DeVry University since 1992
- **Languages** — Native English and Spanish, proficient Italian, conversational French

---

## Highlights

- Object Oriented Time Series class with full ARIMA/SARIMAX forecasting pipeline
- LLM API comparison — OpenAI (`gpt-4o-mini`) and Anthropic (`claude-sonnet-4-5`) side by side
- Kaggle classification vignettes — Logistic Regression, K-NN, Naive Bayes, SVM with K-Fold and Grid Search
- Multivariate time series models (VAR) in `use_cases`
- All notebooks updated for Python 3.14 / macOS M5 compatibility (April 2025)

---

## Getting Started

### Clone this repository

```bash
# Navigate to your projects folder
cd ~/GitHub

# Clone the repo
git clone https://github.com/otrevizo/Python.git

# Enter the repo
cd Python
```

### Set up your Python environment

```bash
# Create a virtual environment
python3 -m venv myenv

# Activate it (macOS / Linux)
source myenv/bin/activate

# Install core dependencies
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels pmdarima
pip install openai anthropic jupyterlab
```

### Launch JupyterLab

```bash
jupyter lab
```

---

## Git Workflow

For a full git command reference see [`git_cheatsheet.md`](git_cheatsheet.md)
in this repo, and the official git guides at https://github.com/git-guides.

The everyday workflow:

```bash
git add <file>                   # Stage a file
git commit -m "Your message"     # Commit with a clear message
git push                         # Push to GitHub
```

Check status at any time:

```bash
git status                       # What has changed?
git log --oneline                # Recent commit history
```

---

## Contact

- **GitHub** — [otrevizo](https://github.com/otrevizo)
- **LinkedIn** — [otrevizo](https://linkedin.com/in/otrevizo)

---

*This portfolio is actively maintained. Feedback and questions welcome.*
