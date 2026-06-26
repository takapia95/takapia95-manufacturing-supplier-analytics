import os
import random
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_part_categories():
    categories = [
        ("CAT001", "Electrical", "Electrical and electronic vehicle components"),
        ("CAT002", "Engine", "Engine and powertrain components"),
        ("CAT003", "Interior", "Interior trim and cabin components"),
        ("CAT004", "Exterior", "Exterior body and trim components"),
        ("CAT005", "Chassis", "Frame, suspension, and structural components"),
        ("CAT006", "Braking", "Brake system components"),
        ("CAT007", "Transmission", "Transmission and drivetrain components"),
        ("CAT008", "Fasteners", "Bolts, clips, screws, and fastening components"),
        ("CAT009", "HVAC", "Heating, ventilation, and air conditioning parts"),
        ("CAT010", "Battery", "Battery and EV-related components"),
        ("CAT011", "Safety", "Airbag, sensor, and safety components"),
        ("CAT012", "Lighting", "Headlamp, taillight, and lighting assemblies")
    ]

    return pd.DataFrame(categories, columns=[
        "PartCategoryID",
        "CategoryName",
        "Description"
    ])


def generate_parts(suppliers_df, categories_df, n=1000):
    part_names_by_category = {
        "Electrical": ["ECU Module", "Wiring Harness", "Sensor Assembly", "Fuse Box", "Control Unit"],
        "Engine": ["Engine Block", "Cylinder Head", "Oil Pump", "Timing Chain", "Fuel Injector"],
        "Interior": ["Door Panel", "Seat Frame", "Dashboard Trim", "Center Console", "Carpet Set"],
        "Exterior": ["Front Bumper", "Rear Bumper", "Side Mirror", "Fender Panel", "Grille Assembly"],
        "Chassis": ["Control Arm", "Subframe", "Suspension Link", "Crossmember", "Stabilizer Bar"],
        "Braking": ["Brake Rotor", "Brake Caliper", "Brake Pad Set", "ABS Module", "Brake Hose"],
        "Transmission": ["Transmission Case", "Clutch Assembly", "Gear Set", "Drive Shaft", "Torque Converter"],
        "Fasteners": ["Bolt Set", "Clip Set", "Screw Pack", "Washer Kit", "Retainer Clip"],
        "HVAC": ["AC Compressor", "Blower Motor", "Evaporator Core", "Heater Core", "Air Duct"],
        "Battery": ["Battery Module", "Battery Tray", "Battery Cable", "Cell Connector", "Cooling Plate"],
        "Safety": ["Airbag Module", "Seatbelt Assembly", "Impact Sensor", "Crash Sensor", "Safety Controller"],
        "Lighting": ["Headlamp Assembly", "Taillight Assembly", "Fog Lamp", "LED Module", "Light Housing"]
    }

    materials = [
        "Steel", "Aluminum", "Plastic", "Rubber", "Copper",
        "Composite", "Glass", "Foam", "Fabric", "Lithium-Ion"
    ]

    suppliers = suppliers_df["SupplierID"].tolist()
    categories = categories_df.to_dict("records")

    rows = []

    for i in range(1, n + 1):
        category = random.choice(categories)
        category_name = category["CategoryName"]

        base_name = random.choice(part_names_by_category[category_name])
        part_name = f"{base_name} {random.randint(100, 999)}"

        unit_cost = round(np.random.lognormal(mean=3.5, sigma=0.8), 2)

        if category_name in ["Engine", "Transmission", "Battery", "Safety"]:
            critical_part = random.choices([True, False], weights=[70, 30])[0]
            unit_cost = round(unit_cost * random.uniform(2.0, 5.0), 2)
        else:
            critical_part = random.choices([True, False], weights=[20, 80])[0]

        rows.append({
            "PartID": f"PRT{i:04d}",
            "SupplierID": random.choice(suppliers),
            "PartCategoryID": category["PartCategoryID"],
            "PartName": part_name,
            "Material": random.choice(materials),
            "UnitCost": unit_cost,
            "CriticalPart": critical_part,
            "PartStatus": random.choices(
                ["Active", "Inactive", "Obsolete"],
                weights=[90, 7, 3]
            )[0]
        })

    return pd.DataFrame(rows)


def main():
    suppliers_path = f"{OUTPUT_DIR}/suppliers.csv"

    if not os.path.exists(suppliers_path):
        raise FileNotFoundError(
            "Missing suppliers.csv. Run generate_master_data.py first."
        )

    suppliers = pd.read_csv(suppliers_path)

    categories = generate_part_categories()
    parts = generate_parts(suppliers, categories)

    categories.to_csv(f"{OUTPUT_DIR}/part_categories.csv", index=False)
    parts.to_csv(f"{OUTPUT_DIR}/parts.csv", index=False)

    print("Product data generated successfully.")
    print(f"Part Categories: {len(categories)}")
    print(f"Parts: {len(parts)}")


if __name__ == "__main__":
    main()