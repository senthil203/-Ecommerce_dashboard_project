"""
E-Commerce Sales Analytics Dashboard
Step 4: Generate formatted Excel Report with multiple sheets
Run: python excel_report.py
"""

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import (PatternFill, Font, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.series import DataPoint
import os

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/ecommerce_sales.csv", parse_dates=["order_date"])
delivered = df[df["order_status"] == "Delivered"].copy()

# ── Helper: style header row ───────────────────────────────────────────────────
HEADER_FILL  = PatternFill("solid", fgColor="185FA5")
HEADER_FONT  = Font(color="FFFFFF", bold=True, size=11)
ALT_FILL     = PatternFill("solid", fgColor="EBF3FC")
BORDER_STYLE = Side(style="thin", color="CCCCCC")
THIN_BORDER  = Border(left=BORDER_STYLE, right=BORDER_STYLE,
                      top=BORDER_STYLE, bottom=BORDER_STYLE)

def style_header(ws, row=1):
    for cell in ws[row]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = THIN_BORDER

def auto_width(ws, padding=4):
    for col in ws.columns:
        max_len = max((len(str(c.value or "")) for c in col), default=8)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + padding, 40)

def alt_rows(ws, start_row, end_row, ncols):
    for r in range(start_row, end_row + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = THIN_BORDER
            if r % 2 == 0:
                cell.fill = ALT_FILL

# ── Build summary DataFrames ───────────────────────────────────────────────────
monthly = (delivered.groupby(delivered["order_date"].dt.to_period("M"))
           .agg(orders=("order_id", "count"),
                revenue=("total_amount", "sum"),
                avg_order=("total_amount", "mean")).reset_index())
monthly["order_date"] = monthly["order_date"].astype(str)
monthly["revenue"]    = monthly["revenue"].round(2)
monthly["avg_order"]  = monthly["avg_order"].round(2)

cat_summary = (delivered.groupby("category")
               .agg(orders=("order_id", "count"),
                    units_sold=("quantity", "sum"),
                    revenue=("total_amount", "sum"),
                    avg_discount=("discount_pct", "mean")).reset_index()
               .sort_values("revenue", ascending=False))
cat_summary["revenue"]      = cat_summary["revenue"].round(2)
cat_summary["avg_discount"] = cat_summary["avg_discount"].round(1)

region_summary = (delivered.groupby("region")
                  .agg(orders=("order_id", "count"),
                       revenue=("total_amount", "sum"),
                       avg_order=("total_amount", "mean"),
                       customers=("customer_id", "nunique")).reset_index()
                  .sort_values("revenue", ascending=False))
region_summary["revenue"]   = region_summary["revenue"].round(2)
region_summary["avg_order"] = region_summary["avg_order"].round(2)

top_products = (delivered.groupby(["product", "category"])
                .agg(units=("quantity", "sum"),
                     revenue=("total_amount", "sum")).reset_index()
                .sort_values("revenue", ascending=False).head(10))
top_products["revenue"] = top_products["revenue"].round(2)

status_summary = (df.groupby("order_status")
                  .agg(orders=("order_id", "count"),
                       revenue=("total_amount", "sum")).reset_index()
                  .sort_values("orders", ascending=False))
status_summary["revenue"] = status_summary["revenue"].round(2)
status_summary["pct"]     = (status_summary["orders"] /
                              status_summary["orders"].sum() * 100).round(1)

# ── Write to Excel ─────────────────────────────────────────────────────────────
output_path = "outputs/ecommerce_report.xlsx"
os.makedirs("outputs", exist_ok=True)

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

    # ── Sheet 1: Raw Data ─────────────────────────────────────────────────────
    df.to_excel(writer, sheet_name="Raw Data", index=False)

    # ── Sheet 2: Monthly Trend ────────────────────────────────────────────────
    monthly.to_excel(writer, sheet_name="Monthly Trend", index=False)

    # ── Sheet 3: Category Summary ─────────────────────────────────────────────
    cat_summary.to_excel(writer, sheet_name="Category Summary", index=False)

    # ── Sheet 4: Regional Performance ────────────────────────────────────────
    region_summary.to_excel(writer, sheet_name="Regional Performance", index=False)

    # ── Sheet 5: Top Products ─────────────────────────────────────────────────
    top_products.to_excel(writer, sheet_name="Top Products", index=False)

    # ── Sheet 6: Order Status ─────────────────────────────────────────────────
    status_summary.to_excel(writer, sheet_name="Order Status", index=False)

# ── Apply styling ──────────────────────────────────────────────────────────────
wb = load_workbook(output_path)

for sname in wb.sheetnames:
    ws = wb[sname]
    style_header(ws, row=1)
    nrows = ws.max_row
    ncols = ws.max_column
    alt_rows(ws, 2, nrows, ncols)
    auto_width(ws)
    ws.freeze_panes = "A2"

# ── Dashboard KPI sheet ────────────────────────────────────────────────────────
ws_kpi = wb.create_sheet("KPI Dashboard", 0)
ws_kpi.sheet_view.showGridLines = False

kpis = [
    ("Total Orders",        f"{len(df):,}"),
    ("Delivered Orders",    f"{len(delivered):,}"),
    ("Unique Customers",    f"{df['customer_id'].nunique():,}"),
    ("Gross Revenue",       f"₹{delivered['total_amount'].sum():,.0f}"),
    ("Total Discounts",     f"₹{delivered['discount_amt'].sum():,.0f}"),
    ("Avg Order Value",     f"₹{delivered['total_amount'].mean():,.0f}"),
    ("Top Category",        delivered.groupby('category')['total_amount'].sum().idxmax()),
    ("Top Region",          delivered.groupby('region')['total_amount'].sum().idxmax()),
    ("Return Rate",         f"{(df['order_status']=='Returned').mean()*100:.1f}%"),
    ("Delivery Rate",       f"{(df['order_status']=='Delivered').mean()*100:.1f}%"),
]

ws_kpi["A1"] = "E-COMMERCE SALES ANALYTICS — KPI DASHBOARD"
ws_kpi["A1"].font      = Font(size=16, bold=True, color="185FA5")
ws_kpi["A1"].alignment = Alignment(horizontal="left")
ws_kpi.merge_cells("A1:D1")

ws_kpi["A2"] = "Full Year 2023  |  Dataset: 2,000 orders  |  All figures for Delivered orders"
ws_kpi["A2"].font      = Font(size=10, color="888888", italic=True)
ws_kpi.merge_cells("A2:D2")

DARK_FILL = PatternFill("solid", fgColor="0D3A6A")
CARD_FILL  = PatternFill("solid", fgColor="EBF3FC")

for idx, (label, value) in enumerate(kpis):
    row = 4 + idx
    ws_kpi.cell(row=row, column=1, value=label).font  = Font(size=10, color="555555")
    val_cell                                           = ws_kpi.cell(row=row, column=2, value=value)
    val_cell.font                                      = Font(size=11, bold=True, color="185FA5")
    val_cell.alignment                                 = Alignment(horizontal="right")
    for c in [1, 2]:
        ws_kpi.cell(row=row, column=c).fill   = CARD_FILL
        ws_kpi.cell(row=row, column=c).border = THIN_BORDER

ws_kpi.column_dimensions["A"].width = 22
ws_kpi.column_dimensions["B"].width = 22

wb.save(output_path)
print(f"✅ Excel report saved: {output_path}")
print(f"   Sheets: {wb.sheetnames}")
