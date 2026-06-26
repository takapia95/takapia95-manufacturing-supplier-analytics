import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = "root"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "supplier_quality_analytics"

DATA_DIR = "data/generated"

engine = create_engine(
    "mysql+pymysql://root@127.0.0.1:3306/supplier_quality_analytics"
)

load_order = [
    ("suppliers.csv", "Suppliers"),
    ("supplier_contacts.csv", "SupplierContacts"),
    ("plants.csv", "Plants"),
    ("production_lines.csv", "ProductionLines"),
    ("employees.csv", "Employees"),
    ("part_categories.csv", "PartCategories"),
    ("parts.csv", "Parts"),
    ("purchase_orders.csv", "PurchaseOrders"),
    ("purchase_order_lines.csv", "PurchaseOrderLines"),
    ("deliveries.csv", "Deliveries"),
    ("inspections.csv", "Inspections"),
    ("defect_categories.csv", "DefectCategories"),
    ("root_causes.csv", "RootCauses"),
    ("defects.csv", "Defects"),
    ("corrective_actions.csv", "CorrectiveActions"),
    ("supplier_audits.csv", "SupplierAudits"),
    ("inventory.csv", "Inventory"),
    ("monthly_supplier_kpis.csv", "MonthlySupplierKPIs"),
]


def clean_dataframe(df):
    df = df.replace({pd.NA: None})
    df = df.where(pd.notnull(df), None)

    for col in df.columns:
        if df[col].dtype == "bool":
            df[col] = df[col].astype(int)

    return df


def main():
    print("Connecting to MySQL...")

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        for _, table_name in reversed(load_order):
            print(f"Clearing table: {table_name}")
            conn.execute(text(f"TRUNCATE TABLE {table_name};"))

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    for csv_file, table_name in load_order:
        path = os.path.join(DATA_DIR, csv_file)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing file: {path}")

        print(f"Loading {csv_file} into {table_name}...")

        df = pd.read_csv(path)
        df = clean_dataframe(df)

        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False
        )

        print(f"Loaded {len(df)} rows into {table_name}")

    print("\nAll CSV files loaded into MySQL successfully.")


if __name__ == "__main__":
    main()
