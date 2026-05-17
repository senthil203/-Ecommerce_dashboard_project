"""
E-Commerce Sales Analytics Dashboard
Step 1: Generate realistic synthetic dataset
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────────
NUM_ORDERS    = 2000
START_DATE    = datetime(2023, 1, 1)
END_DATE      = datetime(2023, 12, 31)
OUTPUT_DIR    = "data"

# ── Reference data ─────────────────────────────────────────────────────────────
CATEGORIES = {
    "Electronics":  ["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch"],
    "Clothing":     ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers"],
    "Books":        ["Python Book", "Data Science Guide", "SQL Handbook", "BA Essentials"],
    "Home & Kitchen":["Coffee Maker", "Blender", "Air Fryer", "Vacuum Cleaner"],
    "Sports":       ["Yoga Mat", "Dumbbell Set", "Running Shoes", "Cycling Helmet"],
}

PRICE_RANGES = {
    "Electronics":   (5000,  80000),
    "Clothing":      (300,   5000),
    "Books":         (150,   1200),
    "Home & Kitchen":(800,   15000),
    "Sports":        (400,   8000),
}

REGIONS   = ["North", "South", "East", "West", "Central"]
CITIES    = {
    "North":  ["Delhi", "Chandigarh", "Amritsar"],
    "South":  ["Chennai", "Bangalore", "Hyderabad"],
    "East":   ["Kolkata", "Bhubaneswar", "Patna"],
    "West":   ["Mumbai", "Pune", "Ahmedabad"],
    "Central":["Bhopal", "Indore", "Nagpur"],
}
GENDERS   = ["Male", "Female", "Other"]
STATUSES  = ["Delivered", "Returned", "Cancelled", "Pending"]
STATUS_WT = [0.78, 0.10, 0.08, 0.04]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


# ── Build dataset ──────────────────────────────────────────────────────────────
rows = []
for i in range(1, NUM_ORDERS + 1):
    category        = random.choice(list(CATEGORIES.keys()))
    product         = random.choice(CATEGORIES[category])
    low, high       = PRICE_RANGES[category]
    unit_price      = round(random.uniform(low, high), 2)
    quantity        = random.randint(1, 5)
    discount_pct    = random.choice([0, 0, 0, 5, 10, 15, 20])
    discount_amt    = round(unit_price * quantity * discount_pct / 100, 2)
    total_amount    = round(unit_price * quantity - discount_amt, 2)

    region          = random.choice(REGIONS)
    city            = random.choice(CITIES[region])
    age             = random.randint(18, 65)
    gender          = random.choices(GENDERS, weights=[0.52, 0.45, 0.03])[0]
    status          = random.choices(STATUSES, weights=STATUS_WT)[0]
    payment         = random.choice(PAYMENT_METHODS)
    order_date      = random_date(START_DATE, END_DATE)

    rows.append({
        "order_id":       f"ORD{i:05d}",
        "customer_id":    f"CUST{random.randint(1, 800):04d}",
        "order_date":     order_date.strftime("%Y-%m-%d"),
        "month":          order_date.strftime("%B"),
        "quarter":        f"Q{(order_date.month - 1) // 3 + 1}",
        "product":        product,
        "category":       category,
        "unit_price":     unit_price,
        "quantity":       quantity,
        "discount_pct":   discount_pct,
        "discount_amt":   discount_amt,
        "total_amount":   total_amount,
        "region":         region,
        "city":           city,
        "customer_age":   age,
        "customer_gender":gender,
        "payment_method": payment,
        "order_status":   status,
    })

df = pd.DataFrame(rows)
df["order_date"] = pd.to_datetime(df["order_date"])
df = df.sort_values("order_date").reset_index(drop=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)
csv_path = os.path.join(OUTPUT_DIR, "ecommerce_sales.csv")
df.to_csv(csv_path, index=False)

print(f"✅ Dataset generated: {len(df)} records")
print(f"   Saved to: {csv_path}")
print(f"\nColumn overview:")
print(df.dtypes)
print(f"\nSample rows:")
print(df.head(3).to_string())
