import os
import random
from datetime import timedelta
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_purchase_orders(suppliers_df, plants_df, n=20000):
    rows = []

    supplier_ids = suppliers_df["SupplierID"].tolist()
    plant_ids = plants_df["PlantID"].tolist()

    for i in range(1, n + 1):
        order_date = fake.date_between(start_date="-2y", end_date="today")
        due_date = order_date + timedelta(days=random.randint(7, 45))

        rows.append({
            "PO_ID": f"PO{i:06d}",
            "SupplierID": random.choice(supplier_ids),
            "PlantID": random.choice(plant_ids),
            "OrderDate": order_date,
            "DueDate": due_date,
            "POStatus": random.choices(
                ["Open", "Closed", "Delayed", "Cancelled"],
                weights=[15, 75, 8, 2]
            )[0],
            "TotalAmount": 0
        })

    return pd.DataFrame(rows)


def generate_purchase_order_lines(purchase_orders_df, parts_df, n=80000):
    rows = []

    po_ids = purchase_orders_df["PO_ID"].tolist()
    part_records = parts_df.to_dict("records")

    for i in range(1, n + 1):
        po_id = random.choice(po_ids)
        part = random.choice(part_records)

        ordered_qty = random.randint(50, 5000)
        unit_cost = float(part["UnitCost"])
        line_total = round(ordered_qty * unit_cost, 2)

        rows.append({
            "POLineID": f"POL{i:06d}",
            "PO_ID": po_id,
            "PartID": part["PartID"],
            "OrderedQuantity": ordered_qty,
            "UnitCost": unit_cost,
            "LineTotal": line_total
        })

    return pd.DataFrame(rows)


def update_purchase_order_totals(purchase_orders_df, po_lines_df):
    totals = (
        po_lines_df
        .groupby("PO_ID")["LineTotal"]
        .sum()
        .reset_index()
        .rename(columns={"LineTotal": "CalculatedTotal"})
    )

    purchase_orders_df = purchase_orders_df.merge(
        totals,
        on="PO_ID",
        how="left"
    )

    purchase_orders_df["TotalAmount"] = (
        purchase_orders_df["CalculatedTotal"]
        .fillna(0)
        .round(2)
    )

    purchase_orders_df = purchase_orders_df.drop(columns=["CalculatedTotal"])

    return purchase_orders_df


def main():
    required_files = [
        "suppliers.csv",
        "plants.csv",
        "parts.csv"
    ]

    for file in required_files:
        path = f"{OUTPUT_DIR}/{file}"
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing {file}. Run previous data generation scripts first."
            )

    suppliers = pd.read_csv(f"{OUTPUT_DIR}/suppliers.csv")
    plants = pd.read_csv(f"{OUTPUT_DIR}/plants.csv")
    parts = pd.read_csv(f"{OUTPUT_DIR}/parts.csv")

    purchase_orders = generate_purchase_orders(suppliers, plants)
    po_lines = generate_purchase_order_lines(purchase_orders, parts)
    purchase_orders = update_purchase_order_totals(purchase_orders, po_lines)

    purchase_orders.to_csv(f"{OUTPUT_DIR}/purchase_orders.csv", index=False)
    po_lines.to_csv(f"{OUTPUT_DIR}/purchase_order_lines.csv", index=False)

    print("Procurement data generated successfully.")
    print(f"Purchase Orders: {len(purchase_orders)}")
    print(f"Purchase Order Lines: {len(po_lines)}")
    print(f"Total PO Value: ${purchase_orders['TotalAmount'].sum():,.2f}")


if __name__ == "__main__":
    main()