import os
import random
from datetime import timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_deliveries(po_lines_df, purchase_orders_df, n=40000):
    rows = []

    po_info = purchase_orders_df.set_index("PO_ID").to_dict("index")
    po_lines = po_lines_df.to_dict("records")

    for i in range(1, n + 1):
        line = random.choice(po_lines)
        po = po_info[line["PO_ID"]]

        due_date = pd.to_datetime(po["DueDate"]).date()

        delay_days = random.choices(
            [0, 1, 2, 3, 5, 7, 10, 14],
            weights=[65, 10, 8, 6, 4, 3, 2, 2]
        )[0]

        delivery_date = due_date + timedelta(days=delay_days)

        received_quantity = random.randint(
            max(1, int(line["OrderedQuantity"] * 0.3)),
            int(line["OrderedQuantity"])
        )

        rejected_quantity = random.choices(
            [0, 0, 0, 1, 2, 5, 10, 20],
            weights=[65, 15, 10, 3, 3, 2, 1, 1]
        )[0]

        rejected_quantity = min(rejected_quantity, received_quantity)

        rows.append({
            "DeliveryID": f"DEL{i:06d}",
            "POLineID": line["POLineID"],
            "DeliveryDate": delivery_date,
            "ReceivedQuantity": received_quantity,
            "RejectedQuantity": rejected_quantity,
            "DelayDays": delay_days,
            "OnTimeFlag": delay_days == 0
        })

    return pd.DataFrame(rows)


def generate_inspections(deliveries_df, employees_df):
    rows = []

    inspectors = employees_df[
        employees_df["Department"].isin(["Quality", "Engineering"])
    ]["EmployeeID"].tolist()

    if not inspectors:
        inspectors = employees_df["EmployeeID"].tolist()

    for i, delivery in deliveries_df.iterrows():
        inspected_quantity = delivery["ReceivedQuantity"]

        base_failed = delivery["RejectedQuantity"]

        additional_failed = random.choices(
            [0, 0, 1, 2, 5, 10],
            weights=[70, 15, 5, 4, 4, 2]
        )[0]

        failed_quantity = min(
            inspected_quantity,
            base_failed + additional_failed
        )

        passed_quantity = inspected_quantity - failed_quantity

        if failed_quantity == 0:
            inspection_score = round(random.uniform(95, 100), 2)
            result = "Pass"
        elif failed_quantity / inspected_quantity <= 0.03:
            inspection_score = round(random.uniform(80, 94), 2)
            result = "Minor Issue"
        else:
            inspection_score = round(random.uniform(50, 79), 2)
            result = "Fail"

        inspection_date = pd.to_datetime(delivery["DeliveryDate"]).date()

        rows.append({
            "InspectionID": f"INS{i + 1:06d}",
            "DeliveryID": delivery["DeliveryID"],
            "InspectorID": random.choice(inspectors),
            "InspectionDate": inspection_date,
            "InspectedQuantity": inspected_quantity,
            "PassedQuantity": passed_quantity,
            "FailedQuantity": failed_quantity,
            "InspectionScore": inspection_score,
            "InspectionResult": result
        })

    return pd.DataFrame(rows)


def main():
    required_files = [
        "purchase_order_lines.csv",
        "purchase_orders.csv",
        "employees.csv"
    ]

    for file in required_files:
        path = f"{OUTPUT_DIR}/{file}"
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing {file}. Run previous generation scripts first."
            )

    po_lines = pd.read_csv(f"{OUTPUT_DIR}/purchase_order_lines.csv")
    purchase_orders = pd.read_csv(f"{OUTPUT_DIR}/purchase_orders.csv")
    employees = pd.read_csv(f"{OUTPUT_DIR}/employees.csv")

    deliveries = generate_deliveries(po_lines, purchase_orders)
    inspections = generate_inspections(deliveries, employees)

    deliveries.to_csv(f"{OUTPUT_DIR}/deliveries.csv", index=False)
    inspections.to_csv(f"{OUTPUT_DIR}/inspections.csv", index=False)

    print("Operations data generated successfully.")
    print(f"Deliveries: {len(deliveries)}")
    print(f"Inspections: {len(inspections)}")
    print(f"Failed Inspections: {(inspections['InspectionResult'] == 'Fail').sum()}")
    print(f"Minor Issues: {(inspections['InspectionResult'] == 'Minor Issue').sum()}")


if __name__ == "__main__":
    main()