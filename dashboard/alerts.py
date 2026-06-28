import pandas as pd

from dashboard.rules import (
    QUALITY_WARNING,
    OTD_WARNING,
    PPM_WARNING_MAX,
)


def generate_alerts(df):
    alerts = []

    if df.empty:
        return alerts

    # -----------------------
    # Quality Alerts
    # -----------------------
    if "AvgQualityScore" in df.columns:

        poor = df[df["AvgQualityScore"] < QUALITY_WARNING]

        for _, row in poor.iterrows():
            alerts.append({
                "Severity": "Critical",
                "Category": "Quality",
                "Supplier": row["SupplierName"],
                "Message": f'Quality Score is {row["AvgQualityScore"]:.1f}'
            })

    # -----------------------
    # Delivery Alerts
    # -----------------------
    if "AvgOnTimeDeliveryRate" in df.columns:

        late = df[df["AvgOnTimeDeliveryRate"] < OTD_WARNING]

        for _, row in late.iterrows():
            alerts.append({
                "Severity": "Warning",
                "Category": "Delivery",
                "Supplier": row["SupplierName"],
                "Message": f'On-Time Delivery {row["AvgOnTimeDeliveryRate"]:.1f}%'
            })

    # -----------------------
    # PPM Alerts
    # -----------------------
    if "AvgPPM" in df.columns:

        ppm = df[df["AvgPPM"] > PPM_WARNING_MAX]

        for _, row in ppm.iterrows():
            alerts.append({
                "Severity": "Critical",
                "Category": "Defects",
                "Supplier": row["SupplierName"],
                "Message": f'PPM = {row["AvgPPM"]:.0f}'
            })

    return pd.DataFrame(alerts)