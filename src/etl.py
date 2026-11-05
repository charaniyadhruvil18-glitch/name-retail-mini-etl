
import pandas as pd
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DB_DIR = ROOT / "db"

RAW_FILE = RAW_DIR / "orders.csv"
CLEAN_FILE = PROCESSED_DIR / "orders_clean.csv"
DB_FILE = DB_DIR / "orders.db"


def create_sample_data():
    """Create synthetic orders if raw data does not exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not RAW_FILE.exists():
        data = {
            "order_id": range(1, 31),
            "order_date": ["2026-11-01"] * 30,
            "product": [
                "Laptop", "Phone", "Tablet", "Headphones", "Monitor"
            ] * 6,
            "quantity": [
                2, 1, 3, None, 2, 1, 4, 2, None, 1,
                3, 2, 1, 5, 2, 1, None, 3, 2, 1,
                4, 2, 1, 3, 2, None, 1, 4, 2, 1
            ],
            "unit_price": [
                500, 300, 200, 50, 150,
                500, 300, 200, 50, 150,
                500, 300, 200, 50, 150,
                500, 300, 200, 50, 150,
                500, 300, 200, 50, 150,
                500, 300, 200, 50, 150
            ]
        }

        pd.DataFrame(data).to_csv(RAW_FILE, index=False)


def run_etl():
    create_sample_data()

    df = pd.read_csv(RAW_FILE)

    df["quantity"] = df["quantity"].fillna(1).astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    df["revenue"] = df["quantity"] * df["unit_price"]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(CLEAN_FILE, index=False)

    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql("orders_clean", conn, if_exists="replace", index=False)

    total_orders = len(df)
    total_revenue = df["revenue"].sum()
    top_product = (
        df.groupby("product")["revenue"]
        .sum()
        .idxmax()
    )

    print("ETL completed successfully!")
    print(f"total_orders: {total_orders}")
    print(f"total_revenue: {total_revenue:.2f}")
    print(f"top_product_by_revenue: {top_product}")


if __name__ == "__main__":
    run_etl()
