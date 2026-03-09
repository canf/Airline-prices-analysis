"""
Airline Ticket Prices — Data Analytics Project
================================================
Tools  : Python, SQLite, Pandas, Matplotlib, Seaborn
Dataset: airline_ticket_prices_dataset.csv (250 records)

Questions answered
------------------
Q1. Which airline has the highest average ticket price?
Q2. How does ticket class affect price distribution?
Q3. Does booking earlier lead to lower prices?
Q4. What are the top 10 most expensive routes?
Q5. Which ticket class offers the best value per km?
"""

import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

# ── Output directory ─────────────────────────────────────────────
os.makedirs("output", exist_ok=True)

# ── Colour palette ───────────────────────────────────────────────
BG       = "#0D1117"
CARD     = "#161B22"
ACCENT   = "#58A6FF"
GOLD     = "#F0A500"
EMERALD  = "#3FB950"
ROSE     = "#FF7B72"
MUTED    = "#8B949E"
WHITE    = "#E6EDF3"
CLASS_COLORS = {"Economy": EMERALD, "Business": ACCENT, "First": GOLD}
CLASS_ORDER  = ["Economy", "Business", "First"]

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   CARD,
    "axes.edgecolor":   "#30363D",
    "axes.labelcolor":  WHITE,
    "xtick.color":      MUTED,
    "ytick.color":      MUTED,
    "text.color":       WHITE,
    "grid.color":       "#21262D",
    "grid.linewidth":   0.6,
    "font.family":      "DejaVu Sans",
})

# ════════════════════════════════════════════════════════════════
# 1. LOAD DATA
# ════════════════════════════════════════════════════════════════
print("Loading data …")
df = pd.read_csv("airline_ticket_prices_dataset.csv")
print(f"  Shape : {df.shape}")
print(f"  Cols  : {list(df.columns)}\n")

# ── SQLite in-memory database ────────────────────────────────────
conn = sqlite3.connect(":memory:")
df.to_sql("tickets", conn, if_exists="replace", index=False)
print("SQLite table 'tickets' created.\n")


# ════════════════════════════════════════════════════════════════
# HELPER
# ════════════════════════════════════════════════════════════════
def run_sql(query: str) -> pd.DataFrame:
    """Execute a SQL query and return the result as a DataFrame."""
    return pd.read_sql(query, conn)


# ════════════════════════════════════════════════════════════════
# Q1 — Which airline has the highest average ticket price?
# ════════════════════════════════════════════════════════════════
print("─" * 60)
print("Q1 · Average ticket price by airline")
print("─" * 60)

SQL_Q1 = """
    SELECT Airline,
           ROUND(AVG(Price_USD), 2) AS Avg_Price,
           COUNT(*)                 AS Tickets
    FROM   tickets
    GROUP  BY Airline
    ORDER  BY Avg_Price DESC;
"""

q1 = run_sql(SQL_Q1)
print(q1.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
colors = [GOLD if i == 0 else ACCENT for i in range(len(q1))]
bars = ax.barh(q1["Airline"], q1["Avg_Price"], color=colors, height=0.55, zorder=3)
ax.bar_label(bars, labels=[f"${v:,.0f}" for v in q1["Avg_Price"]],
             padding=6, color=WHITE, fontsize=10, fontweight="bold")
ax.set_xlabel("Average Ticket Price (USD)", labelpad=10)
ax.set_title("Q1 · Which Airline Has the Highest Average Ticket Price?",
             fontsize=13, fontweight="bold", color=WHITE, pad=14)
ax.invert_yaxis()
ax.xaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.set_xlim(0, q1["Avg_Price"].max() * 1.22)
plt.tight_layout()
plt.savefig("output/q1_avg_price_by_airline.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("  → Saved: output/q1_avg_price_by_airline.png\n")


# ════════════════════════════════════════════════════════════════
# Q2 — How does ticket class affect price distribution?
# ════════════════════════════════════════════════════════════════
print("─" * 60)
print("Q2 · Price distribution by ticket class")
print("─" * 60)

SQL_Q2 = """
    SELECT Class,
           ROUND(AVG(Price_USD), 2) AS Avg_Price,
           ROUND(MIN(Price_USD), 2) AS Min_Price,
           ROUND(MAX(Price_USD), 2) AS Max_Price
    FROM   tickets
    GROUP  BY Class
    ORDER  BY Avg_Price DESC;
"""

q2 = run_sql(SQL_Q2)
print(q2.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
data_by_class = [df[df["Class"] == c]["Price_USD"].values for c in CLASS_ORDER]
bp = ax.boxplot(
    data_by_class,
    patch_artist=True,
    medianprops=dict(color=WHITE, linewidth=2),
    whiskerprops=dict(color=MUTED),
    capprops=dict(color=MUTED),
    flierprops=dict(marker="o", color=MUTED, markersize=4, alpha=0.5),
)
for patch, cls in zip(bp["boxes"], CLASS_ORDER):
    patch.set_facecolor(CLASS_COLORS[cls])
    patch.set_alpha(0.82)
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(CLASS_ORDER, fontsize=12)
ax.set_ylabel("Ticket Price (USD)"); ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.set_title("Q2 · How Does Ticket Class Affect Price?",
             fontsize=13, fontweight="bold", color=WHITE, pad=14)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
for i, (cls, row) in enumerate(zip(CLASS_ORDER, q2.itertuples()), 1):
    ax.text(i, ax.get_ylim()[1] * 0.97, f"avg ${row.Avg_Price:,.0f}",
            ha="center", va="top", fontsize=9, color=CLASS_COLORS[cls], fontweight="bold")
plt.tight_layout()
plt.savefig("output/q2_price_by_class.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("  → Saved: output/q2_price_by_class.png\n")


# ════════════════════════════════════════════════════════════════
# Q3 — Does booking earlier lead to lower prices?
# ════════════════════════════════════════════════════════════════
print("─" * 60)
print("Q3 · Price vs. days before departure")
print("─" * 60)

SQL_Q3 = """
    SELECT Days_Before_Departure,
           ROUND(AVG(Price_USD), 2) AS Avg_Price,
           Class
    FROM   tickets
    GROUP  BY Days_Before_Departure, Class
    ORDER  BY Days_Before_Departure;
"""

q3 = run_sql(SQL_Q3)
print(q3.head(10).to_string(index=False), "\n  …")

fig, ax = plt.subplots(figsize=(11, 5), facecolor=BG)
for cls in CLASS_ORDER:
    sub = df[df["Class"] == cls].sort_values("Days_Before_Departure")
    ax.scatter(sub["Days_Before_Departure"], sub["Price_USD"],
               color=CLASS_COLORS[cls], alpha=0.35, s=18, zorder=3)
    z = np.polyfit(sub["Days_Before_Departure"], sub["Price_USD"], 1)
    xs = np.linspace(sub["Days_Before_Departure"].min(),
                     sub["Days_Before_Departure"].max(), 200)
    ax.plot(xs, np.poly1d(z)(xs), color=CLASS_COLORS[cls],
            linewidth=2.2, label=cls, zorder=4)
ax.set_xlabel("Days Before Departure"); ax.set_ylabel("Price (USD)")
ax.set_title("Q3 · Does Booking Earlier Lead to Lower Prices?",
             fontsize=13, fontweight="bold", color=WHITE, pad=14)
ax.legend(framealpha=0.15, edgecolor="#30363D", fontsize=10)
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
plt.tight_layout()
plt.savefig("output/q3_booking_timing.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("  → Saved: output/q3_booking_timing.png\n")


# ════════════════════════════════════════════════════════════════
# Q4 — Top 10 most expensive routes
# ════════════════════════════════════════════════════════════════
print("─" * 60)
print("Q4 · Top 10 most expensive routes (≥3 tickets)")
print("─" * 60)

SQL_Q4 = """
    SELECT Origin || ' → ' || Destination AS Route,
           ROUND(AVG(Price_USD), 2)        AS Avg_Price,
           COUNT(*)                         AS Tickets
    FROM   tickets
    GROUP  BY Origin, Destination
    HAVING Tickets >= 3
    ORDER  BY Avg_Price DESC
    LIMIT  10;
"""

q4 = run_sql(SQL_Q4)
print(q4.to_string(index=False))

colors_q4 = [GOLD, GOLD, ACCENT, ACCENT, ACCENT, ROSE, ROSE, ROSE, ROSE, EMERALD]
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
bars = ax.barh(q4["Route"], q4["Avg_Price"], color=colors_q4, height=0.6, zorder=3)
ax.bar_label(bars, labels=[f"${v:,.0f}" for v in q4["Avg_Price"]],
             padding=6, color=WHITE, fontsize=9.5, fontweight="bold")
ax.invert_yaxis()
ax.set_xlabel("Average Price (USD)")
ax.set_title("Q4 · Top 10 Most Expensive Routes (min 3 tickets)",
             fontsize=13, fontweight="bold", color=WHITE, pad=14)
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.set_xlim(0, q4["Avg_Price"].max() * 1.2)
plt.tight_layout()
plt.savefig("output/q4_top_routes.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("  → Saved: output/q4_top_routes.png\n")


# ════════════════════════════════════════════════════════════════
# Q5 — Which ticket class offers the best value per km?
# ════════════════════════════════════════════════════════════════
print("─" * 60)
print("Q5 · Price per km by ticket class")
print("─" * 60)

SQL_Q5 = """
    SELECT Class,
           ROUND(AVG(Price_USD * 1.0 / Distance_km), 4) AS Price_Per_Km,
           ROUND(AVG(Price_USD), 2)                      AS Avg_Price,
           ROUND(AVG(Distance_km), 0)                    AS Avg_Distance
    FROM   tickets
    GROUP  BY Class
    ORDER  BY Price_Per_Km;
"""

q5 = run_sql(SQL_Q5)
print(q5.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(11, 5), facecolor=BG)

# Left: price per km bar
ax = axes[0]
b = ax.bar(q5["Class"], q5["Price_Per_Km"],
           color=[CLASS_COLORS[c] for c in q5["Class"]], width=0.5, zorder=3)
ax.bar_label(b, labels=[f"${v:.3f}/km" for v in q5["Price_Per_Km"]],
             padding=4, color=WHITE, fontsize=10, fontweight="bold")
ax.set_ylabel("USD per km"); ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.set_title("Price Efficiency (USD/km)", fontsize=11, color=WHITE)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.set_ylim(0, q5["Price_Per_Km"].max() * 1.3)

# Right: normalised price vs distance
ax2 = axes[1]
x = np.arange(3)
norm_price = q5["Avg_Price"] / q5["Avg_Price"].max()
norm_dist  = q5["Avg_Distance"] / q5["Avg_Distance"].max()
w = 0.32
ax2.bar(x - w / 2, norm_price, w, label="Norm. Avg Price",
        color=[CLASS_COLORS[c] for c in q5["Class"]], alpha=0.9, zorder=3)
ax2.bar(x + w / 2, norm_dist, w, label="Norm. Avg Distance",
        color=[CLASS_COLORS[c] for c in q5["Class"]], alpha=0.45, hatch="//", zorder=3)
ax2.set_xticks(x); ax2.set_xticklabels(q5["Class"])
ax2.set_title("Price vs Distance (normalised)", fontsize=11, color=WHITE)
ax2.yaxis.grid(True); ax2.set_axisbelow(True)
ax2.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax2.legend(framealpha=0.15, edgecolor="#30363D", fontsize=9)

fig.suptitle("Q5 · Which Ticket Class Offers the Best Value per km?",
             fontsize=13, fontweight="bold", color=WHITE, y=1.01)
plt.tight_layout()
plt.savefig("output/q5_value_per_km.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("  → Saved: output/q5_value_per_km.png\n")


# ════════════════════════════════════════════════════════════════
# DONE
# ════════════════════════════════════════════════════════════════
conn.close()
print("=" * 60)
print("All analyses complete. Charts saved to ./output/")
print("=" * 60)
