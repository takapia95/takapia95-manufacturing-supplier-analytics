import os
import random
from datetime import date
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_suppliers(n=100):
    categories = ["Electronics", "Metal", "Plastic", "Fasteners", "Interior", "Exterior", "Powertrain"]
    risk_levels = ["Low", "Medium", "High"]

    rows = []

    for i in range(1, n + 1):
        supplier_id = f"SUP{i:03d}"

        rows.append({
            "SupplierID": supplier_id,
            "SupplierName": fake.company(),
            "SupplierCategory": random.choice(categories),
            "Country": "USA",
            "State": random.choice(["GA", "AL", "TN", "SC", "NC", "KY", "MI", "OH"]),
            "City": fake.city(),
            "ISO9001Certified": random.choice([True, True, True, False]),
            "IATF16949Certified": random.choice([True, True, False]),
            "PreferredSupplier": random.choice([True, False]),
            "RiskLevel": random.choices(risk_levels, weights=[60, 30, 10])[0],
            "SupplierStatus": random.choices(["Active", "Inactive"], weights=[95, 5])[0],
            "StartDate": fake.date_between(start_date="-10y", end_date="-1y")
        })

    return pd.DataFrame(rows)


def generate_supplier_contacts(suppliers_df):
    rows = []

    for supplier_id in suppliers_df["SupplierID"]:
        contact_count = random.randint(1, 3)

        for i in range(contact_count):
            rows.append({
                "ContactID": f"CON{len(rows) + 1:04d}",
                "SupplierID": supplier_id,
                "ContactName": fake.name(),
                "JobTitle": random.choice([
                    "Quality Manager",
                    "Sales Manager",
                    "Account Manager",
                    "Supplier Representative",
                    "Operations Manager"
                ]),
                "Email": fake.email(),
                "Phone": fake.phone_number()
            })

    return pd.DataFrame(rows)


def generate_plants():
    rows = [
        {
            "PlantID": "PLT001",
            "PlantName": "West Point Assembly Plant",
            "City": "West Point",
            "State": "GA",
            "Country": "USA",
            "PlantType": "Assembly",
            "OpeningDate": "2009-01-01"
        },
        {
            "PlantID": "PLT002",
            "PlantName": "Montgomery Powertrain Plant",
            "City": "Montgomery",
            "State": "AL",
            "Country": "USA",
            "PlantType": "Engine",
            "OpeningDate": "2010-06-15"
        },
        {
            "PlantID": "PLT003",
            "PlantName": "Savannah Parts Distribution Center",
            "City": "Savannah",
            "State": "GA",
            "Country": "USA",
            "PlantType": "Distribution",
            "OpeningDate": "2015-03-20"
        },
        {
            "PlantID": "PLT004",
            "PlantName": "Columbus Components Plant",
            "City": "Columbus",
            "State": "GA",
            "Country": "USA",
            "PlantType": "Assembly",
            "OpeningDate": "2012-09-10"
        },
        {
            "PlantID": "PLT005",
            "PlantName": "Chattanooga Assembly Plant",
            "City": "Chattanooga",
            "State": "TN",
            "Country": "USA",
            "PlantType": "Assembly",
            "OpeningDate": "2011-05-18"
        },
        {
            "PlantID": "PLT006",
            "PlantName": "Louisville Battery Plant",
            "City": "Louisville",
            "State": "KY",
            "Country": "USA",
            "PlantType": "Battery",
            "OpeningDate": "2018-11-05"
        }
    ]

    return pd.DataFrame(rows)


def generate_production_lines(plants_df):
    rows = []
    shifts = ["Day", "Evening", "Night"]

    for _, plant in plants_df.iterrows():
        for line_num in range(1, 5):
            rows.append({
                "LineID": f"LIN{len(rows) + 1:03d}",
                "PlantID": plant["PlantID"],
                "LineName": f"{plant['PlantName']} Line {line_num}",
                "Shift": random.choice(shifts),
                "CapacityPerDay": random.randint(400, 1200),
                "Status": random.choices(["Active", "Maintenance", "Offline"], weights=[85, 10, 5])[0]
            })

    return pd.DataFrame(rows)


def generate_employees(plants_df, n=200):
    departments = ["Quality", "Purchasing", "Production", "Engineering", "Logistics", "Management"]
    job_titles = {
        "Quality": ["Quality Inspector", "Supplier Quality Engineer", "Quality Manager"],
        "Purchasing": ["Buyer", "Purchasing Analyst", "Procurement Manager"],
        "Production": ["Production Supervisor", "Line Operator", "Production Manager"],
        "Engineering": ["Process Engineer", "Manufacturing Engineer", "Industrial Engineer"],
        "Logistics": ["Logistics Coordinator", "Warehouse Supervisor", "Materials Planner"],
        "Management": ["Plant Manager", "Operations Manager", "Director of Manufacturing"]
    }

    rows = []

    for i in range(1, n + 1):
        department = random.choice(departments)

        rows.append({
            "EmployeeID": f"EMP{i:04d}",
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "JobTitle": random.choice(job_titles[department]),
            "Department": department,
            "PlantID": random.choice(plants_df["PlantID"].tolist()),
            "HireDate": fake.date_between(start_date="-12y", end_date="-30d"),
            "EmploymentStatus": random.choices(["Active", "Leave", "Retired"], weights=[92, 5, 3])[0]
        })

    return pd.DataFrame(rows)


def main():
    suppliers = generate_suppliers()
    contacts = generate_supplier_contacts(suppliers)
    plants = generate_plants()
    production_lines = generate_production_lines(plants)
    employees = generate_employees(plants)

    suppliers.to_csv(f"{OUTPUT_DIR}/suppliers.csv", index=False)
    contacts.to_csv(f"{OUTPUT_DIR}/supplier_contacts.csv", index=False)
    plants.to_csv(f"{OUTPUT_DIR}/plants.csv", index=False)
    production_lines.to_csv(f"{OUTPUT_DIR}/production_lines.csv", index=False)
    employees.to_csv(f"{OUTPUT_DIR}/employees.csv", index=False)

    print("Master data generated successfully.")
    print(f"Suppliers: {len(suppliers)}")
    print(f"Supplier Contacts: {len(contacts)}")
    print(f"Plants: {len(plants)}")
    print(f"Production Lines: {len(production_lines)}")
    print(f"Employees: {len(employees)}")


if __name__ == "__main__":
    main()