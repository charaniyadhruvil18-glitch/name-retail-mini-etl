
import pandas as pd
from src.etl import run_etl, CLEAN_FILE


def test_revenue_column_exists_and_non_negative():
    run_etl()
    df = pd.read_csv(CLEAN_FILE)

    assert "revenue" in df.columns
    assert (df["revenue"] >= 0).all()


def test_missing_quantity_filled_with_one():
    run_etl()
    df = pd.read_csv(CLEAN_FILE)

    assert df["quantity"].notna().all()
    assert (df["quantity"] >= 1).all()
