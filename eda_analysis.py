"""
E-Commerce Sales Analytics Dashboard
Step 3: Exploratory Data Analysis + 6 Business Charts
Run: python eda_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/ecommerce_sales.csv", parse_dates=["order_date"])
delivered = df[df["order_status"] == "Delivered"].copy()

os.makedirs("outputs", exist_ok=True)

# ── Styling ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "figure.dpi":        150,
})

PALETTE = ["#185FA5", "#1D9E75", "#D85A30", "#7F77DD", "#BA7517", "#D4537E"]


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Monthly Revenue Trend (line chart)
# ══════════════════════════════════════════════════════════════════════════════
monthly = (delivered.groupby(delivered["order_date"].dt.to_period("M"))
           ["total_amount"].sum().reset_index())
monthly["order_date"] = monthly["order_date"].astype(str)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["order_date"], monthly["total_amount"] / 1e6,
        marker="o", color=PALETTE[0], linewidth=2.5, markersize=5)
ax.fill_between(range(len(monthly)), monthly["total_amount"] / 1e6,
                alpha=0.15, color=PALETTE[0])
ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly["order_date"], rotation=45, ha="right", fontsize=9)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.1f}M"))
ax.set_title("Monthly Revenue Trend (Delivered Orders)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (₹ Millions)")
plt.tight_layout()
plt.savefig("outputs/chart1_monthly_revenue.png", bbox_inches="tight")
plt.close()
print("✅ Chart 1 saved: Monthly Revenue Trend")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 — Revenue by Category (horizontal bar)
# ══════════════════════════════════════════════════════════════════════════════
cat_rev = (delivered.groupby("category")["total_amount"]
           .sum().sort_values(ascending=True))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(cat_rev.index, cat_rev.values / 1e6,
               color=PALETTE[:len(cat_rev)], height=0.55)
for bar, val in zip(bars, cat_rev.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            f"₹{val/1e6:.1f}M", va="center", fontsize=10, fontweight="bold",
            color="#333")
ax.set_xlabel("Revenue (₹ Millions)")
ax.set_title("Revenue by Product Category", fontsize=14, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}M"))
plt.tight_layout()
plt.savefig("outputs/chart2_category_revenue.png", bbox_inches="tight")
plt.close()
print("✅ Chart 2 saved: Category Revenue")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 — Regional Performance (donut chart)
# ══════════════════════════════════════════════════════════════════════════════
region_rev = delivered.groupby("region")["total_amount"].sum()

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    region_rev, labels=region_rev.index, autopct="%1.1f%%",
    colors=PALETTE, startangle=140,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight("bold")
ax.set_title("Revenue Distribution by Region", fontsize=14, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("outputs/chart3_regional_revenue.png", bbox_inches="tight")
plt.close()
print("✅ Chart 3 saved: Regional Revenue")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 — Top 10 Products by Revenue (bar chart)
# ══════════════════════════════════════════════════════════════════════════════
top_products = (delivered.groupby("product")["total_amount"]
                .sum().nlargest(10).sort_values(ascending=True))

fig, ax = plt.subplots(figsize=(10, 6))
colors = [PALETTE[0] if i >= len(top_products) - 3 else "#B5D4F4"
          for i in range(len(top_products))]
bars = ax.barh(top_products.index, top_products.values / 1e6,
               color=colors, height=0.55)
for bar, val in zip(bars, top_products.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            f"₹{val/1e6:.1f}M", va="center", fontsize=9, color="#333")
ax.set_xlabel("Revenue (₹ Millions)")
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("outputs/chart4_top_products.png", bbox_inches="tight")
plt.close()
print("✅ Chart 4 saved: Top 10 Products")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 5 — Order Status Breakdown (stacked bar by quarter)
# ══════════════════════════════════════════════════════════════════════════════
status_q = (df.groupby(["quarter", "order_status"])["order_id"]
            .count().unstack(fill_value=0))
status_colors = {"Delivered": PALETTE[1], "Returned": PALETTE[2],
                 "Cancelled": PALETTE[3], "Pending": PALETTE[4]}

fig, ax = plt.subplots(figsize=(9, 5))
bottom = np.zeros(len(status_q))
for status, color in status_colors.items():
    if status in status_q.columns:
        ax.bar(status_q.index, status_q[status], bottom=bottom,
               label=status, color=color, width=0.55, edgecolor="white")
        bottom += status_q[status].values
ax.set_title("Order Status by Quarter", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Quarter")
ax.set_ylabel("Number of Orders")
ax.legend(title="Status", bbox_to_anchor=(1, 1), loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig("outputs/chart5_order_status.png", bbox_inches="tight")
plt.close()
print("✅ Chart 5 saved: Order Status by Quarter")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 6 — Payment Method Distribution (bar)
# ══════════════════════════════════════════════════════════════════════════════
pay = (delivered.groupby("payment_method")["order_id"]
       .count().sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(pay.index, pay.values, color=PALETTE, width=0.55, edgecolor="white")
for bar, val in zip(bars, pay.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
            str(val), ha="center", fontsize=10, fontweight="bold", color="#333")
ax.set_title("Orders by Payment Method", fontsize=14, fontweight="bold", pad=12)
ax.set_ylabel("Number of Orders")
ax.set_xlabel("Payment Method")
plt.tight_layout()
plt.savefig("outputs/chart6_payment_methods.png", bbox_inches="tight")
plt.close()
print("✅ Chart 6 saved: Payment Methods")


# ══════════════════════════════════════════════════════════════════════════════
# Print Summary KPIs to Console
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 50)
print("   BUSINESS KPI SUMMARY")
print("═" * 50)
print(f"  Total Orders       : {len(df):,}")
print(f"  Delivered Orders   : {len(delivered):,}")
print(f"  Unique Customers   : {df['customer_id'].nunique():,}")
print(f"  Gross Revenue      : ₹{delivered['total_amount'].sum():,.0f}")
print(f"  Total Discounts    : ₹{delivered['discount_amt'].sum():,.0f}")
print(f"  Avg Order Value    : ₹{delivered['total_amount'].mean():,.0f}")
print(f"  Top Category       : {delivered.groupby('category')['total_amount'].sum().idxmax()}")
print(f"  Top Region         : {delivered.groupby('region')['total_amount'].sum().idxmax()}")
print("═" * 50)
print(f"\nAll charts saved to: outputs/")
