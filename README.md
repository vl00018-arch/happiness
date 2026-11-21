# World Happiness Report — EDA (2015–2019)
DSCI 101-001 · Introduction to Data Science · West Virginia University

## Setup (VS Code + uv)
```bash
uv venv elation
source elation/bin/activate          # macOS / Linux
# elation\Scripts\activate           # Windows
uv pip install -r requirements.txt
plotly_get_chrome                     # one-time, lets plotly save map PNGs
```
In VS Code: `Ctrl/Cmd+Shift+P` → **Python: Select Interpreter** → pick `elation`.

## Run
Put the five yearly files in `data/` as `2015.csv` … `2019.csv`, then:
```bash
python happiness_eda.py
```
Or open `happiness_eda.py` in VS Code and click **Run Cell** above each `# %%`.

## Output
- `images/` — every figure (Tasks 1–4, 6–9), plus interactive HTML for the 3D plot and world map
- `results/` — tables as CSV (summary stats, missing countries, correlations, region ranks)

## Data
The raw data files are confidential and are **not** included in this repository (see `.gitignore`).
