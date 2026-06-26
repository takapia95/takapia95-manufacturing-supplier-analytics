import os
import random
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_supplier_audits(suppliers_df, employees_df, n=500):
    auditors = employees_df[
        employees_df["Department"].isin(["Quality", "Engineering", "Management"])
    ]["EmployeeID"].tolist()

    if not auditors:
        auditors = employees_df["EmployeeID"].tolist()

    rows = []

    for i in range(1, n + 1):
        audit_score = round(random.uniform(55, 100), 2)

        if audit_score >= 85:
            audit_result = "Pass"
            major_findings = random.randint(0, 1)
            minor_findings = random.randint(0, 3)
        elif audit_score >= 70:
            audit_result = "Conditional"
            major_findings = random.randint(1, 2)
            minor_findings = random.randint(2, 6)
        else:
            audit_result = "Fail"
            major_findings = random.randint(2, 5)
            minor_findings = random.randint(4, 10)

        rows.append({
            "AuditID": f"AUD{i:06d}",
            "SupplierID": random.choice(suppliers_df["SupplierID"].tolist()),
            "AuditorID": random.choice(auditors),
            "AuditDate": fake.date_between(start_date="-2y", end_date="today"),
            "AuditScore": audit_score,
            "MajorFindings": major_findings,
            "MinorFindings": minor_findings,
            "AuditResult": audit_result
        })

    return pd.DataFrame(rows)


def generate_inventory(parts_df, plants_df, n=5000):
    rows = []

    parts = parts_df["PartID"].tolist()
    plants = plants_df["PlantID"].tolist()

    for i in range(1, n + 1):
        safety_stock = random.randint(100, 2000)
        reorder_level = int(safety_stock * random.uniform(0.6, 0.9))
        current_stock = random.randint(0, safety_stock * 4)

        rows.append({
            "InventoryID": f"INV{i:06d}",
            "PartID": random.choice(parts),
            "PlantID": random.choice(plants),
            "CurrentStock": current_stock,
            "SafetyStock": safety_stock,
            "ReorderLevel": reorder_level,
            "LastUpdated": fake.date_between(start_date="-90d", end_date="today")
        })

    return pd.DataFrame(rows)


def generate_monthly_supplier_kpis(
    suppliers_df,
    purchase_orders_df,
    po_lines_df,
    deliveries_df,
    inspections_df,
    defects_df,
    corrective_actions_df,
    supplier_audits_df
):
    rows = []

    po_supplier = purchase_orders_df[["PO_ID", "SupplierID"]]
    line_po = po_lines_df[["POLineID", "PO_ID"]]

    delivery_supplier = (
        deliveries_df
        .merge(line_po, on="POLineID", how="left")
        .merge(po_supplier, on="PO_ID", how="left")
    )

    delivery_supplier["DeliveryMonth"] = pd.to_datetime(
        delivery_supplier["DeliveryDate"]
    ).dt.to_period("M").dt.to_timestamp()

    inspection_delivery = inspections_df[[
        "InspectionID",
        "DeliveryID",
        "FailedQuantity",
        "InspectionScore"
    ]]

    inspection_supplier = (
        inspection_delivery
        .merge(delivery_supplier[[
            "DeliveryID",
            "SupplierID",
            "ReceivedQuantity",
            "OnTimeFlag",
            "DeliveryMonth"
        ]], on="DeliveryID", how="left")
    )

    defects_enriched = (
        defects_df
        .merge(inspection_supplier[[
            "InspectionID",
            "SupplierID",
            "DeliveryMonth"
        ]], on="InspectionID", how="left")
    )

    car_counts = (
        corrective_actions_df[
            corrective_actions_df["Status"].isin(["Open", "In Progress", "Overdue"])
        ]
        .groupby("SupplierID")
        .size()
        .reset_index(name="OpenCARCount")
    )

    latest_audit = (
        supplier_audits_df
        .sort_values("AuditDate")
        .groupby("SupplierID")
        .tail(1)[["SupplierID", "AuditScore"]]
    )

    supplier_months = (
        delivery_supplier[["SupplierID", "DeliveryMonth"]]
        .dropna()
        .drop_duplicates()
    )

    for _, row in supplier_months.iterrows():
        supplier_id = row["SupplierID"]
        month = row["DeliveryMonth"]

        supplier_deliveries = delivery_supplier[
            (delivery_supplier["SupplierID"] == supplier_id) &
            (delivery_supplier["DeliveryMonth"] == month)
        ]

        supplier_inspections = inspection_supplier[
            (inspection_supplier["SupplierID"] == supplier_id) &
            (inspection_supplier["DeliveryMonth"] == month)
        ]

        supplier_defects = defects_enriched[
            (defects_enriched["SupplierID"] == supplier_id) &
            (defects_enriched["DeliveryMonth"] == month)
        ]

        total_received = int(supplier_deliveries["ReceivedQuantity"].sum())
        total_defective = int(supplier_inspections["FailedQuantity"].sum())

        ppm = round(
            (total_defective / total_received) * 1_000_000,
            2
        ) if total_received > 0 else 0

        on_time_rate = round(
            supplier_deliveries["OnTimeFlag"].mean() * 100,
            2
        ) if len(supplier_deliveries) > 0 else 0

        avg_inspection_score = round(
            supplier_inspections["InspectionScore"].mean(),
            2
        ) if len(supplier_inspections) > 0 else 0

        scrap_cost = round(
            supplier_defects["DefectCost"].sum(),
            2
        ) if len(supplier_defects) > 0 else 0

        open_car_count = 0
        car_match = car_counts[car_counts["SupplierID"] == supplier_id]
        if not car_match.empty:
            open_car_count = int(car_match["OpenCARCount"].iloc[0])

        audit_score = 85
        audit_match = latest_audit[latest_audit["SupplierID"] == supplier_id]
        if not audit_match.empty:
            audit_score = float(audit_match["AuditScore"].iloc[0])

        quality_score = max(0, 100 - (ppm / 200))
        delivery_score = on_time_rate
        car_score = max(0, 100 - (open_car_count * 5))

        supplier_quality_score = round(
            (quality_score * 0.40) +
            (delivery_score * 0.25) +
            (audit_score * 0.20) +
            (car_score * 0.15),
            2
        )

        if supplier_quality_score >= 90:
            risk_level = "Low"
        elif supplier_quality_score >= 75:
            risk_level = "Medium"
        elif supplier_quality_score >= 60:
            risk_level = "High"
        else:
            risk_level = "Critical"

        rows.append({
            "KPI_ID": f"KPI{len(rows) + 1:06d}",
            "SupplierID": supplier_id,
            "Month": month.date(),
            "TotalReceived": total_received,
            "TotalDefective": total_defective,
            "PPM": ppm,
            "OnTimeDeliveryRate": on_time_rate,
            "AverageInspectionScore": avg_inspection_score,
            "ScrapCost": scrap_cost,
            "OpenCARCount": open_car_count,
            "SupplierQualityScore": supplier_quality_score,
            "RiskLevel": risk_level
        })

    return pd.DataFrame(rows)


def main():
    required_files = [
        "suppliers.csv",
        "employees.csv",
        "parts.csv",
        "plants.csv",
        "purchase_orders.csv",
        "purchase_order_lines.csv",
        "deliveries.csv",
        "inspections.csv",
        "defects.csv",
        "corrective_actions.csv"
    ]

    for file in required_files:
        path = f"{OUTPUT_DIR}/{file}"
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing {file}. Run previous generation scripts first."
            )

    suppliers = pd.read_csv(f"{OUTPUT_DIR}/suppliers.csv")
    employees = pd.read_csv(f"{OUTPUT_DIR}/employees.csv")
    parts = pd.read_csv(f"{OUTPUT_DIR}/parts.csv")
    plants = pd.read_csv(f"{OUTPUT_DIR}/plants.csv")
    purchase_orders = pd.read_csv(f"{OUTPUT_DIR}/purchase_orders.csv")
    po_lines = pd.read_csv(f"{OUTPUT_DIR}/purchase_order_lines.csv")
    deliveries = pd.read_csv(f"{OUTPUT_DIR}/deliveries.csv")
    inspections = pd.read_csv(f"{OUTPUT_DIR}/inspections.csv")
    defects = pd.read_csv(f"{OUTPUT_DIR}/defects.csv")
    corrective_actions = pd.read_csv(f"{OUTPUT_DIR}/corrective_actions.csv")

    supplier_audits = generate_supplier_audits(suppliers, employees)
    inventory = generate_inventory(parts, plants)
    monthly_kpis = generate_monthly_supplier_kpis(
        suppliers,
        purchase_orders,
        po_lines,
        deliveries,
        inspections,
        defects,
        corrective_actions,
        supplier_audits
    )

    supplier_audits.to_csv(f"{OUTPUT_DIR}/supplier_audits.csv", index=False)
    inventory.to_csv(f"{OUTPUT_DIR}/inventory.csv", index=False)
    monthly_kpis.to_csv(f"{OUTPUT_DIR}/monthly_supplier_kpis.csv", index=False)

    print("Reporting data generated successfully.")
    print(f"Supplier Audits: {len(supplier_audits)}")
    print(f"Inventory Records: {len(inventory)}")
    print(f"Monthly Supplier KPIs: {len(monthly_kpis)}")


if __name__ == "__main__":
    main()