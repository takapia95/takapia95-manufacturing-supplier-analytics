import os
import random
from datetime import timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_defect_categories():
    categories = [
        ("DEF001", "Scratch", "Surface scratch or cosmetic damage"),
        ("DEF002", "Crack", "Cracked material or structural weakness"),
        ("DEF003", "Dent", "Visible dent or deformation"),
        ("DEF004", "Dimension Out of Spec", "Part dimension does not meet tolerance"),
        ("DEF005", "Missing Component", "Required component is missing"),
        ("DEF006", "Electrical Failure", "Electrical part does not function correctly"),
        ("DEF007", "Weld Failure", "Poor or failed weld condition"),
        ("DEF008", "Paint Defect", "Paint issue, discoloration, or uneven coating"),
        ("DEF009", "Rust", "Corrosion or oxidation found"),
        ("DEF010", "Incorrect Label", "Wrong, missing, or unreadable label"),
        ("DEF011", "Packaging Damage", "Damage caused by poor packaging"),
        ("DEF012", "Contamination", "Foreign material or contamination found")
    ]

    return pd.DataFrame(categories, columns=[
        "DefectCategoryID",
        "DefectName",
        "Description"
    ])


def generate_root_causes():
    root_causes = [
        ("RC001", "Machine Calibration", "Machine was not calibrated correctly"),
        ("RC002", "Operator Error", "Incorrect handling or assembly by operator"),
        ("RC003", "Poor Packaging", "Packaging did not protect parts during shipment"),
        ("RC004", "Material Defect", "Raw material quality issue"),
        ("RC005", "Process Variation", "Manufacturing process variation outside control limits"),
        ("RC006", "Supplier Process Change", "Supplier changed process without proper validation"),
        ("RC007", "Tool Wear", "Worn tooling caused quality issue"),
        ("RC008", "Maintenance Issue", "Machine or equipment maintenance issue"),
        ("RC009", "Incorrect Specification", "Wrong specification or drawing used"),
        ("RC010", "Handling Damage", "Damage occurred during handling or transport")
    ]

    return pd.DataFrame(root_causes, columns=[
        "RootCauseID",
        "RootCauseName",
        "Description"
    ])


def generate_defects(inspections_df, defect_categories_df, root_causes_df, parts_df):
    rows = []

    failed_inspections = inspections_df[
        inspections_df["FailedQuantity"] > 0
    ].copy()

    defect_categories = defect_categories_df.to_dict("records")
    root_causes = root_causes_df.to_dict("records")

    avg_unit_cost = float(parts_df["UnitCost"].mean())

    defect_id = 1

    for _, inspection in failed_inspections.iterrows():
        defect_count = random.choices(
            [1, 2, 3],
            weights=[75, 20, 5]
        )[0]

        remaining_failed_qty = int(inspection["FailedQuantity"])

        for _ in range(defect_count):
            if remaining_failed_qty <= 0:
                break

            defect_category = random.choice(defect_categories)
            root_cause = random.choice(root_causes)

            defect_quantity = random.randint(1, remaining_failed_qty)
            remaining_failed_qty -= defect_quantity

            severity = random.choices(
                ["Minor", "Major", "Critical"],
                weights=[65, 28, 7]
            )[0]

            if severity == "Minor":
                scrap_quantity = random.choices(
                    [0, 0, 1],
                    weights=[80, 15, 5]
                )[0]
            elif severity == "Major":
                scrap_quantity = random.randint(0, defect_quantity)
            else:
                scrap_quantity = random.randint(
                    max(1, defect_quantity // 2),
                    defect_quantity
                )

            scrap_quantity = min(scrap_quantity, defect_quantity)
            rework_quantity = defect_quantity - scrap_quantity

            estimated_cost = (
                scrap_quantity * avg_unit_cost +
                rework_quantity * avg_unit_cost * 0.35
            )

            if severity == "Critical":
                estimated_cost *= 1.75
            elif severity == "Major":
                estimated_cost *= 1.25

            rows.append({
                "DefectID": f"DFT{defect_id:06d}",
                "InspectionID": inspection["InspectionID"],
                "DefectCategoryID": defect_category["DefectCategoryID"],
                "RootCauseID": root_cause["RootCauseID"],
                "DefectQuantity": defect_quantity,
                "Severity": severity,
                "ScrapQuantity": scrap_quantity,
                "ReworkQuantity": rework_quantity,
                "DefectCost": round(estimated_cost, 2)
            })

            defect_id += 1

    return pd.DataFrame(rows)


def generate_corrective_actions(defects_df, inspections_df, deliveries_df, po_lines_df, purchase_orders_df, employees_df):
    rows = []

    quality_employees = employees_df[
        employees_df["Department"].isin(["Quality", "Engineering", "Management"])
    ]["EmployeeID"].tolist()

    if not quality_employees:
        quality_employees = employees_df["EmployeeID"].tolist()

    inspection_delivery = inspections_df[["InspectionID", "DeliveryID", "InspectionDate"]]
    delivery_po_line = deliveries_df[["DeliveryID", "POLineID"]]
    po_line_po = po_lines_df[["POLineID", "PO_ID"]]
    po_supplier = purchase_orders_df[["PO_ID", "SupplierID"]]

    defect_supplier_map = (
        defects_df
        .merge(inspection_delivery, on="InspectionID", how="left")
        .merge(delivery_po_line, on="DeliveryID", how="left")
        .merge(po_line_po, on="POLineID", how="left")
        .merge(po_supplier, on="PO_ID", how="left")
    )

    car_id = 1

    for _, defect in defect_supplier_map.iterrows():
        should_open = False

        if defect["Severity"] == "Critical":
            should_open = True
        elif defect["Severity"] == "Major":
            should_open = random.random() < 0.45
        elif defect["DefectQuantity"] >= 10:
            should_open = random.random() < 0.35

        if not should_open:
            continue

        open_date = pd.to_datetime(defect["InspectionDate"]).date()
        due_date = open_date + timedelta(days=random.choice([14, 30, 45, 60]))

        status = random.choices(
            ["Open", "In Progress", "Closed", "Overdue"],
            weights=[20, 30, 40, 10]
        )[0]

        if status == "Closed":
            close_date = open_date + timedelta(
                days=random.randint(5, max(6, (due_date - open_date).days))
            )
            verification_status = random.choices(
                ["Verified", "Rejected"],
                weights=[90, 10]
            )[0]
        elif status == "Overdue":
            close_date = ""
            verification_status = "Pending"
        else:
            close_date = ""
            verification_status = "Pending"

        action_description = (
            f"Investigate {defect['Severity'].lower()} defect, identify root cause, "
            "implement corrective action, and verify effectiveness."
        )

        rows.append({
            "CAR_ID": f"CAR{car_id:06d}",
            "DefectID": defect["DefectID"],
            "SupplierID": defect["SupplierID"],
            "OpenDate": open_date,
            "DueDate": due_date,
            "CloseDate": close_date,
            "Status": status,
            "OwnerID": random.choice(quality_employees),
            "ActionDescription": action_description,
            "VerificationStatus": verification_status
        })

        car_id += 1

    return pd.DataFrame(rows)


def main():
    required_files = [
        "inspections.csv",
        "deliveries.csv",
        "purchase_order_lines.csv",
        "purchase_orders.csv",
        "employees.csv",
        "parts.csv"
    ]

    for file in required_files:
        path = f"{OUTPUT_DIR}/{file}"
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing {file}. Run previous generation scripts first."
            )

    inspections = pd.read_csv(f"{OUTPUT_DIR}/inspections.csv")
    deliveries = pd.read_csv(f"{OUTPUT_DIR}/deliveries.csv")
    po_lines = pd.read_csv(f"{OUTPUT_DIR}/purchase_order_lines.csv")
    purchase_orders = pd.read_csv(f"{OUTPUT_DIR}/purchase_orders.csv")
    employees = pd.read_csv(f"{OUTPUT_DIR}/employees.csv")
    parts = pd.read_csv(f"{OUTPUT_DIR}/parts.csv")

    defect_categories = generate_defect_categories()
    root_causes = generate_root_causes()
    defects = generate_defects(inspections, defect_categories, root_causes, parts)
    corrective_actions = generate_corrective_actions(
        defects,
        inspections,
        deliveries,
        po_lines,
        purchase_orders,
        employees
    )

    defect_categories.to_csv(f"{OUTPUT_DIR}/defect_categories.csv", index=False)
    root_causes.to_csv(f"{OUTPUT_DIR}/root_causes.csv", index=False)
    defects.to_csv(f"{OUTPUT_DIR}/defects.csv", index=False)
    corrective_actions.to_csv(f"{OUTPUT_DIR}/corrective_actions.csv", index=False)

    print("Quality data generated successfully.")
    print(f"Defect Categories: {len(defect_categories)}")
    print(f"Root Causes: {len(root_causes)}")
    print(f"Defects: {len(defects)}")
    print(f"Corrective Actions: {len(corrective_actions)}")


if __name__ == "__main__":
    main()