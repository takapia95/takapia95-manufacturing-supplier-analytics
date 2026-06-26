import subprocess
import sys

scripts = [
    "etl/generate_master_data.py",
    "etl/generate_product_data.py",
    "etl/generate_procurement_data.py",
    "etl/generate_operations_data.py",
    "etl/generate_quality_data.py",
    "etl/generate_reporting_data.py",
]

for script in scripts:
    print(f"\nRunning {script}...")
    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        print(f"Error running {script}")
        sys.exit(result.returncode)

print("\nAll data generated successfully.")