# %% [markdown]
# # World Happiness Report — Exploratory Data Analysis (2015–2019)
# DSCI 101-001 · Introduction to Data Science · West Virginia University
#
# Run the whole file with `python happiness_eda.py`, or run it cell by cell
# in VS Code (each `# %%` line starts a cell — click "Run Cell").
#
# Every tabular result is rendered through `show()`:
#   - in a notebook / VS Code Interactive Window -> a real rendered table
#   - in a plain terminal                        -> a bordered Markdown table
#
# Expected folder layout:
#   data/2015.csv ... data/2019.csv   (raw files — NOT committed to GitHub)
#   images/                           (all figures are saved here)
#   results/                          (tables saved as CSV)

# %% 0. Setup ---------------------------------------------------------------
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import pycountry
from scipy import stats

DATA_DIR = Path("data")
IMG_DIR = Path("images")
RES_DIR = Path("results")
IMG_DIR.mkdir(exist_ok=True)
RES_DIR.mkdir(exist_ok=True)

YEARS = [2015, 2016, 2017, 2018, 2019]
FACTORS = ["GDP", "Family", "Health", "Freedom", "Corruption", "Generosity"]

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 200)


# Every table shown also accumulates here, and is written to
# results/report.md at the end of the run — one readable file with all
# of it, instead of eight separate CSVs.
REPORT = ["# World Happiness Report — EDA (2015–2019)",
          "DSCI 101-001 · Introduction to Data Science · West Virginia University",
          f"_Generated {pd.Timestamp.now():%Y-%m-%d %H:%M}_"]


def header(title):
    print("\n" + "=" * 80 + f"\n{title}\n" + "=" * 80)
    REPORT.append(f"\n## {title}")


def note(text):
    """A line of prose that belongs in both the console and the report."""
    print(text)
    REPORT.append(text)


# ---- TABLE RENDERING -------------------------------------------------------
def _in_notebook():
    """True in Jupyter / Colab / the VS Code Interactive Window."""
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell is not None and shell.__class__.__name__ != "TerminalInteractiveShell"
    except Exception:
        return False


IN_NOTEBOOK = _in_notebook()


def show(obj, title=None, decimals=3, index=True):
    """Render a DataFrame/Series as a table in whichever environment we're in."""
    if isinstance(obj, pd.Series):
        obj = obj.to_frame()
    if decimals is not None:
        obj = obj.round(decimals)
    if title:
        print(f"\n{title}")
    try:
        md = obj.to_markdown(index=index)
    except ImportError:              # tabulate not installed
        md = None
        print("  [install tabulate for bordered tables: pip install tabulate]")
    if IN_NOTEBOOK:
        from IPython.display import display
        display(obj)
    else:
        print(md if md is not None else obj.to_string(index=index))
    # collect for results/report.md
    if title:
        REPORT.append(f"\n### {title}\n")
    REPORT.append(md if md is not None else "```\n" + obj.to_string(index=index) + "\n```")


def one_based(df):
    """Renumber rows 1..n instead of 0..n-1 (for lists shown as tables)."""
    df = df.reset_index(drop=True)
    df.index = range(1, len(df) + 1)
    df.index.name = "#"
    return df


# %% 1. Load and harmonize the five files ----------------------------------
# Every year uses different column names, so we rename them to one standard set.
COLUMN_MAP = {
    "Country": "Country", "Country or region": "Country",
    "Region": "Region",
    "Happiness Rank": "Rank", "Happiness.Rank": "Rank", "Overall rank": "Rank",
    "Happiness Score": "Score", "Happiness.Score": "Score", "Score": "Score",
    "Economy (GDP per Capita)": "GDP", "Economy..GDP.per.Capita.": "GDP",
    "GDP per capita": "GDP",
    "Family": "Family", "Social support": "Family",
    "Health (Life Expectancy)": "Health", "Health..Life.Expectancy.": "Health",
    "Healthy life expectancy": "Health",
    "Freedom": "Freedom", "Freedom to make life choices": "Freedom",
    "Trust (Government Corruption)": "Corruption",
    "Trust..Government.Corruption.": "Corruption",
    "Perceptions of corruption": "Corruption",
    "Generosity": "Generosity",
}
KEEP = ["Country", "Region", "Rank", "Score"] + FACTORS

# Some countries are spelled differently across years. Without fixing these,
# Task 5 would wrongly report them as "missing".
NAME_FIXES = {
    "Taiwan Province of China": "Taiwan",
    "Hong Kong S.A.R., China": "Hong Kong",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "Northern Cyprus": "North Cyprus",
    "North Macedonia": "Macedonia",
    "Somaliland region": "Somaliland Region",
}


def load_year(year):
    raw = pd.read_csv(DATA_DIR / f"{year}.csv")  # "N/A" is read as NaN
    df = raw.rename(columns=COLUMN_MAP)
    df = df[[c for c in KEEP if c in df.columns]].copy()
    df["RawName"] = df["Country"].str.strip()
    df["Country"] = df["RawName"].replace(NAME_FIXES)
    df["Year"] = year
    return df


data = {y: load_year(y) for y in YEARS}

# 2017–2019 have no Region column -> borrow it from 2015/2016.
region_lookup = (
    pd.concat([data[2015], data[2016]])
    .drop_duplicates("Country")
    .set_index("Country")["Region"]
    .to_dict()
)
region_lookup.update({"Gambia": "Sub-Saharan Africa"})  # only appears in 2019
for y in YEARS:
    data[y]["Region"] = data[y]["Country"].map(region_lookup)

df_all = pd.concat(data.values(), ignore_index=True)

header("DATA OVERVIEW")
overview = df_all.groupby("Year").agg(countries=("Country", "nunique"),
                                      mean_score=("Score", "mean"))
show(overview, "Countries and mean score per year")

missing = df_all[KEEP].isna().sum()
missing = missing[missing > 0].rename("Missing values").to_frame()
missing.index.name = "Column"
show(missing if len(missing) else pd.DataFrame({"Column": ["(none)"]}),
     "Missing values per column (all years)", decimals=None)

no_region = sorted(df_all.loc[df_all["Region"].isna(), "Country"].unique())
show(one_based(pd.DataFrame({"Country": no_region or ["(none)"]})),
     "Countries still without a region", decimals=None)

note("\n**NOTE:** 'Corruption' is the *Trust (Government Corruption)* factor — "
     "a HIGHER value means people perceive LESS corruption.")


# %% Helper: label interesting points on scatter plots ----------------------
def label_points(ax, df, x, y, n_extreme=4, n_outliers=3):
    """Label the happiest/unhappiest countries plus the biggest outliers
    from a straight-line fit (labeling all ~155 countries is unreadable)."""
    d = df.dropna(subset=[x, y])
    slope, intercept = np.polyfit(d[x], d[y], 1)
    resid = (d[y] - (slope * d[x] + intercept)).abs()
    picks = pd.concat([d.nlargest(n_extreme, "Score"),
                       d.nsmallest(n_extreme, "Score"),
                       d.loc[resid.nlargest(n_outliers).index]]).drop_duplicates("Country")
    for _, r in picks.iterrows():
        ax.annotate(r["Country"], (r[x], r[y]), fontsize=7,
                    xytext=(3, 3), textcoords="offset points")
    xs = np.linspace(d[x].min(), d[x].max(), 50)
    ax.plot(xs, slope * xs + intercept, "--", color="gray", lw=1)


def scatter_by_year(x, y, xlabel, ylabel, fname, title):
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    for ax, year in zip(axes.flat, YEARS):
        d = data[year].dropna(subset=[x, y])
        sc = ax.scatter(d[x], d[y], c=d["Score"], cmap="viridis", s=25, alpha=0.8)
        label_points(ax, d, x, y)
        r = d[x].corr(d[y])
        ax.set_title(f"{year}  (Pearson r = {r:.2f})")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(alpha=0.3)
    axes.flat[-1].axis("off")
    fig.colorbar(sc, ax=axes.flat[-1], label="Happiness Score", fraction=0.5)
    fig.suptitle(title, fontsize=16)
    fig.tight_layout()
    fig.savefig(IMG_DIR / fname, dpi=150)
    plt.show()


def corr_by_year(x, y):
    """Per-year Pearson r plus sample size, as a table."""
    rows = []
    for year in YEARS:
        d = data[year][[x, y]].dropna()
        rows.append({"Year": year, "n": len(d), f"Pearson r ({x} vs {y})": d[x].corr(d[y])})
    return pd.DataFrame(rows).set_index("Year")


# %% TASK 1 — Distribution of the Happiness Score ---------------------------
header("TASK 1 — Distribution of Happiness Score")
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
for ax, year in zip(axes.flat, YEARS):
    s = data[year]["Score"]
    ax.hist(s, bins=15, color="steelblue", edgecolor="white")
    ax.axvline(s.mean(), color="red", ls="--", label=f"mean {s.mean():.2f}")
    ax.axvline(s.median(), color="orange", ls=":", label=f"median {s.median():.2f}")
    ax.set_title(str(year))
    ax.set_xlabel("Happiness Score")
    ax.set_ylabel("Number of countries")
    ax.legend(fontsize=8)
# Last panel: all five years overlaid as density curves
for year in YEARS:
    data[year]["Score"].plot.kde(ax=axes.flat[-1], label=str(year))
axes.flat[-1].set_title("All years (density)")
axes.flat[-1].set_xlabel("Happiness Score")
axes.flat[-1].legend()
fig.suptitle("Task 1 — Distribution of Happiness Score by Year", fontsize=16)
fig.tight_layout()
fig.savefig(IMG_DIR / "task1_score_histograms.png", dpi=150)
plt.show()

summary = df_all.groupby("Year")["Score"].describe()
summary["skew"] = df_all.groupby("Year")["Score"].skew()
summary["kurtosis"] = df_all.groupby("Year")["Score"].apply(pd.Series.kurt)
show(summary, "Summary statistics of Happiness Score by year")
summary.round(4).to_csv(RES_DIR / "task1_score_summary.csv")


# %% TASK 2 — GDP per Capita vs Health --------------------------------------
header("TASK 2 — GDP per Capita vs Health (Life Expectancy)")
scatter_by_year("GDP", "Health", "GDP per Capita", "Health (Life Expectancy)",
                "task2_gdp_vs_health.png", "Task 2 — GDP per Capita vs Health")
t2 = corr_by_year("GDP", "Health")
show(t2, "Correlation between GDP per Capita and Health, by year")
t2.round(4).to_csv(RES_DIR / "task2_gdp_health_corr.csv")


# %% TASK 3 — Freedom vs Generosity -----------------------------------------
header("TASK 3 — Freedom vs Generosity")
scatter_by_year("Freedom", "Generosity", "Freedom", "Generosity",
                "task3_freedom_vs_generosity.png", "Task 3 — Freedom vs Generosity")
t3 = corr_by_year("Freedom", "Generosity")
show(t3, "Correlation between Freedom and Generosity, by year")
t3.round(4).to_csv(RES_DIR / "task3_freedom_generosity_corr.csv")


# %% TASK 4 — 3D: GDP, Corruption, Generosity -------------------------------
header("TASK 4 — GDP per Capita, Corruption (Trust), Generosity — 3D")
for year in YEARS:
    d = data[year].dropna(subset=["GDP", "Corruption", "Generosity"])
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")
    sc = ax.scatter(d["GDP"], d["Corruption"], d["Generosity"],
                    c=d["Score"], cmap="viridis", s=30, alpha=0.85)
    # label the 5 happiest, 5 unhappiest, and top-3 most generous / most trusted
    picks = pd.concat([d.nlargest(5, "Score"), d.nsmallest(5, "Score"),
                       d.nlargest(3, "Generosity"), d.nlargest(3, "Corruption")]
                      ).drop_duplicates("Country")
    for _, r in picks.iterrows():
        ax.text(r["GDP"], r["Corruption"], r["Generosity"], r["Country"], fontsize=7)
    ax.set_xlabel("GDP per Capita")
    ax.set_ylabel("Trust (Gov. Corruption)")
    ax.set_zlabel("Generosity")
    ax.set_title(f"Task 4 — GDP vs Corruption vs Generosity ({year})")
    fig.colorbar(sc, label="Happiness Score", shrink=0.6, pad=0.1)
    fig.tight_layout()
    fig.savefig(IMG_DIR / f"task4_3d_{year}.png", dpi=150)
    plt.show()

# Interactive version: hover over any dot to see the country name
fig3d = px.scatter_3d(df_all.dropna(subset=["Corruption"]), x="GDP", y="Corruption",
                      z="Generosity", color="Score", hover_name="Country",
                      animation_frame="Year", color_continuous_scale="Viridis",
                      title="Task 4 — GDP vs Corruption vs Generosity (interactive)")
fig3d.write_html(IMG_DIR / "task4_3d_interactive.html")

rows = []
for y in YEARS:
    c = data[y][["GDP", "Corruption", "Generosity"]].corr()
    rows.append({"Year": y,
                 "GDP–Corruption": c.loc["GDP", "Corruption"],
                 "GDP–Generosity": c.loc["GDP", "Generosity"],
                 "Corruption–Generosity": c.loc["Corruption", "Generosity"]})
t4 = pd.DataFrame(rows).set_index("Year")
show(t4, "Pairwise Pearson correlations by year")
t4.round(4).to_csv(RES_DIR / "task4_pairwise_corr.csv")


# %% TASK 5 — Countries missing between consecutive years -------------------
header("TASK 5 — Countries missing between consecutive years")

renamed = df_all[df_all["RawName"] != df_all["Country"]][["Year", "RawName", "Country"]]
show(one_based(renamed) if len(renamed)
     else pd.DataFrame({"RawName": ["(none)"], "Country": ["(none)"]}),
     "Name changes detected (treated as the same country)", decimals=None)

rows, counts = [], []
for prev, nxt in zip(YEARS[:-1], YEARS[1:]):
    a, b = set(data[prev]["Country"]), set(data[nxt]["Country"])
    dropped, added = sorted(a - b), sorted(b - a)
    counts.append({"Comparison": f"{prev} vs {nxt}",
                   f"n in first year": len(a), "n in second year": len(b),
                   "Dropped": len(dropped), "Added": len(added)})
    rows += [{"Comparison": f"{prev} vs {nxt}", "Country": c,
              "Status": f"missing in {nxt}"} for c in dropped]
    rows += [{"Comparison": f"{prev} vs {nxt}", "Country": c,
              "Status": f"new in {nxt}"} for c in added]

show(pd.DataFrame(counts).set_index("Comparison"),
     "Country count changes between consecutive years", decimals=None)

changes = pd.DataFrame(rows)
show(one_based(changes), "Every country that entered or left the dataset", decimals=None)
changes.to_csv(RES_DIR / "task5_missing_countries.csv", index=False)

in_all = set.intersection(*(set(data[y]["Country"]) for y in YEARS))
note(f"\n**Countries present in all 5 years: {len(in_all)}**")


# %% TASK 6 — Pearson, Spearman, Kendall correlations -----------------------
header("TASK 6 — Pearson, Spearman and Kendall correlation coefficients")
PAIRS = [("Score", "Generosity"), ("Freedom", "Generosity"),
         ("GDP", "Corruption"), ("GDP", "Freedom")]
rows = []
for year in YEARS:
    for x, y in PAIRS:
        d = data[year][[x, y]].dropna()
        pr, pp = stats.pearsonr(d[x], d[y])
        sr, sp = stats.spearmanr(d[x], d[y])
        kt, kp = stats.kendalltau(d[x], d[y])
        rows.append({"Year": year, "Pair": f"{x} & {y}", "n": len(d),
                     "Pearson r": pr, "Pearson p": pp,
                     "Spearman rho": sr, "Spearman p": sp,
                     "Kendall tau": kt, "Kendall p": kp})
corr_table = pd.DataFrame(rows)
corr_table.round(4).to_csv(RES_DIR / "task6_correlations.csv", index=False)

for pair, g in corr_table.groupby("Pair", sort=False):
    show(g.drop(columns="Pair").set_index("Year"), f"{pair}", decimals=4)

# Visual summary: one panel per pair, the three coefficients across years
fig, axes = plt.subplots(1, 4, figsize=(20, 5), sharey=True)
for ax, (pair, g) in zip(axes, corr_table.groupby("Pair", sort=False)):
    for col, m in [("Pearson r", "o"), ("Spearman rho", "s"), ("Kendall tau", "^")]:
        ax.plot(g["Year"], g[col], marker=m, label=col)
    ax.axhline(0, color="gray", lw=0.8)
    ax.set_title(pair)
    ax.set_xticks(YEARS)
    ax.grid(alpha=0.3)
axes[0].set_ylabel("Correlation coefficient")
axes[0].legend()
fig.suptitle("Task 6 — Correlation coefficients by year", fontsize=15)
fig.tight_layout()
fig.savefig(IMG_DIR / "task6_correlations.png", dpi=150)
plt.show()


# %% TASK 7 — Which variables relate most strongly to Happiness? ------------
header("TASK 7 — Variables most strongly related to Happiness Score")
pear = pd.DataFrame({y: data[y][FACTORS].corrwith(data[y]["Score"]) for y in YEARS})
spear = pd.DataFrame({y: data[y][FACTORS].corrwith(data[y]["Score"], method="spearman")
                      for y in YEARS})
pear["Mean"] = pear.mean(axis=1)
spear["Mean"] = spear.mean(axis=1)
pear = pear.sort_values("Mean", ascending=False)
spear = spear.loc[pear.index]
pear.index.name = "Factor"
spear.index.name = "Factor"

show(pear, "Pearson correlation of each factor with Happiness Score")
show(spear, "Spearman correlation of each factor with Happiness Score")

ranking = pear["Mean"].reset_index()
ranking.columns = ["Factor", "Mean Pearson r"]
show(one_based(ranking), "Ranking (strongest -> weakest, by mean Pearson r)")
pear.round(4).to_csv(RES_DIR / "task7_pearson_with_score.csv")

# Heatmap: factor-vs-score correlation for every year
fig, ax = plt.subplots(figsize=(9, 5))
im = ax.imshow(pear.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(pear.shape[1]), pear.columns)
ax.set_yticks(range(pear.shape[0]), pear.index)
for i in range(pear.shape[0]):
    for j in range(pear.shape[1]):
        ax.text(j, i, f"{pear.iat[i, j]:.2f}", ha="center", va="center", fontsize=9)
fig.colorbar(im, label="Pearson r with Happiness Score")
ax.set_title("Task 7 — Correlation of each factor with Happiness Score")
fig.tight_layout()
fig.savefig(IMG_DIR / "task7_factor_score_heatmap.png", dpi=150)
plt.show()

# Full correlation matrix (all years pooled)
cm = df_all[["Score"] + FACTORS].corr()
show(cm, "Full correlation matrix (2015–2019 pooled)")

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(cm.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(cm)), cm.columns, rotation=45, ha="right")
ax.set_yticks(range(len(cm)), cm.index)
for i in range(len(cm)):
    for j in range(len(cm)):
        ax.text(j, i, f"{cm.iat[i, j]:.2f}", ha="center", va="center", fontsize=9)
fig.colorbar(im, label="Pearson r")
ax.set_title("Task 7 — Correlation matrix (2015–2019 pooled)")
fig.tight_layout()
fig.savefig(IMG_DIR / "task7_correlation_matrix.png", dpi=150)
plt.show()


# %% TASK 8 — World map of Happiness Score ----------------------------------
header("TASK 8 — World map (choropleth) of Happiness Score")
ISO_OVERRIDES = {
    "Congo (Kinshasa)": "COD", "Congo (Brazzaville)": "COG", "Ivory Coast": "CIV",
    "Kosovo": "XKX", "Palestinian Territories": "PSE", "Russia": "RUS",
    "South Korea": "KOR", "Laos": "LAO", "Iran": "IRN", "Syria": "SYR",
    "Vietnam": "VNM", "Bolivia": "BOL", "Venezuela": "VEN", "Tanzania": "TZA",
    "Moldova": "MDA", "Macedonia": "MKD", "Swaziland": "SWZ", "Taiwan": "TWN",
    "Czech Republic": "CZE", "Turkey": "TUR",
    "North Cyprus": None, "Somaliland Region": None,  # not recognized states
}


def to_iso3(name):
    if name in ISO_OVERRIDES:
        return ISO_OVERRIDES[name]
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None


df_all["ISO3"] = df_all["Country"].map(to_iso3)
unplaced = sorted(df_all.loc[df_all["ISO3"].isna(), "Country"].unique())
show(one_based(pd.DataFrame({"Country": unplaced or ["(none)"]})),
     "Not placed on the map", decimals=None)

score_range = (df_all["Score"].min(), df_all["Score"].max())

# Interactive map with a year slider
fig_map = px.choropleth(df_all.dropna(subset=["ISO3"]), locations="ISO3",
                        color="Score", hover_name="Country",
                        hover_data={"Rank": True, "ISO3": False},
                        animation_frame="Year", range_color=score_range,
                        color_continuous_scale="RdYlGn",
                        title="Task 8 — World Happiness Score, 2015–2019")
fig_map.write_html(IMG_DIR / "task8_world_map_interactive.html")

# One static PNG per year (needs the `kaleido` package + Chrome, see README)
for year in YEARS:
    d = df_all[(df_all["Year"] == year) & df_all["ISO3"].notna()]
    f = px.choropleth(d, locations="ISO3", color="Score", hover_name="Country",
                      range_color=score_range, color_continuous_scale="RdYlGn",
                      title=f"Task 8 — World Happiness Score ({year})")
    f.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    try:
        f.write_image(IMG_DIR / f"task8_world_map_{year}.png", width=1400, height=750, scale=2)
    except Exception as e:  # kaleido/Chrome missing
        print(f"Could not save PNG for {year} ({type(e).__name__}). "
              "Run `plotly_get_chrome` once, then re-run. HTML map was still saved.")
        break
print("Saved: images/task8_world_map_interactive.html (open in a browser)")


# %% TASK 9 — Happiness rank trends by year and by region -------------------
header("TASK 9 — Happiness rank trends by year and region")
n_countries = df_all.groupby("Year")["Country"].count()
show(n_countries.rename("Ranked countries"), "Number of ranked countries per year",
     decimals=None)

# Because the number of countries changes, we also use a percentile rank
# (0 = happiest, 100 = least happy) so years are comparable.
df_all["RankPct"] = 100 * (df_all["Rank"] - 1) / (df_all["Year"].map(n_countries) - 1)

region_rank = df_all.pivot_table(index="Region", columns="Year", values="Rank", aggfunc="mean")
region_rank["Change 2015→2019 (+ = worse)"] = region_rank[2019] - region_rank[2015]
region_rank = region_rank.sort_values(2019)
show(region_rank, "Mean happiness rank by region (lower = happier)", decimals=1)
region_rank.round(2).to_csv(RES_DIR / "task9_region_mean_rank.csv")

region_score = df_all.pivot_table(index="Region", columns="Year", values="Score", aggfunc="mean")
show(region_score.loc[region_rank.index], "Mean happiness score by region")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
for region, row in region_rank[YEARS].iterrows():
    axes[0].plot(YEARS, row.values, marker="o", label=region)
axes[0].invert_yaxis()  # rank 1 at the top
axes[0].set_title("Mean happiness rank by region (rank 1 = happiest)")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Mean rank")
axes[0].set_xticks(YEARS)
axes[0].grid(alpha=0.3)
axes[0].legend(fontsize=8)

order = region_rank.index.tolist()
box_data = [df_all.loc[df_all["Region"] == r, "Rank"] for r in order]
try:                                   # matplotlib >= 3.11
    axes[1].boxplot(box_data, orientation="horizontal")
except TypeError:                      # older matplotlib
    axes[1].boxplot(box_data, vert=False)
axes[1].set_yticks(range(1, len(order) + 1), order)
axes[1].invert_xaxis()
axes[1].set_title("Spread of ranks within each region (all years)")
axes[1].set_xlabel("Happiness rank")
fig.suptitle("Task 9 — Happiness rank trends by region", fontsize=15)
fig.tight_layout()
fig.savefig(IMG_DIR / "task9_region_rank_trends.png", dpi=150)
plt.show()

# Biggest individual movers between 2015 and 2019
wide = df_all.pivot_table(index="Country", columns="Year", values="Rank").dropna(subset=[2015, 2019])
wide["Change"] = wide[2015] - wide[2019]  # positive = moved UP (happier)
risers = wide.nlargest(10, "Change")
fallers = wide.nsmallest(10, "Change")

show(risers[[2015, 2019, "Change"]].astype(int),
     "Top 10 risers 2015→2019 (positive = moved up)", decimals=None)
show(fallers[[2015, 2019, "Change"]].astype(int),
     "Top 10 fallers 2015→2019", decimals=None)

movers = pd.concat([risers, fallers])["Change"].sort_values()
fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(movers.index, movers.values,
        color=["firebrick" if v < 0 else "seagreen" for v in movers.values])
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Places gained in rank (2015 → 2019)")
ax.set_title("Task 9 — Biggest rank changes, 2015 → 2019")
fig.tight_layout()
fig.savefig(IMG_DIR / "task9_biggest_movers.png", dpi=150)
plt.show()

# %% Write every table collected above into one readable file -------------
REPORT.append("\n---\n\n## Figures\n")
for png in sorted(IMG_DIR.glob("*.png")):
    REPORT.append(f"- `images/{png.name}`")
for html in sorted(IMG_DIR.glob("*.html")):
    REPORT.append(f"- `images/{html.name}` (interactive — open in a browser)")

report_path = RES_DIR / "report.md"
report_path.write_text("\n".join(REPORT) + "\n", encoding="utf-8")

print(f"\nDone. Figures are in images/, tables in results/.")
print(f"All tables in one file: {report_path}")