def generate_executive_narrative(df, alerts_df):
    total_suppliers = len(df)

    avg_quality = df["AvgQualityScore"].mean() if "AvgQualityScore" in df.columns else None
    avg_otd = df["AvgOnTimeDeliveryRate"].mean() if "AvgOnTimeDeliveryRate" in df.columns else None
    avg_ppm = df["AvgPPM"].mean() if "AvgPPM" in df.columns else None

    critical_alerts = 0
    warning_alerts = 0

    if alerts_df is not None and not alerts_df.empty:
        critical_alerts = len(alerts_df[alerts_df["Severity"] == "Critical"])
        warning_alerts = len(alerts_df[alerts_df["Severity"] == "Warning"])

    narrative = (
        f"The current supplier network includes {total_suppliers:,} active suppliers. "
        f"Average supplier quality is {avg_quality:.2f}, average on-time delivery is {avg_otd:.2f}%, "
        f"and average defect exposure is {avg_ppm:.2f} PPM. "
        f"The Executive Alert Center currently identifies {critical_alerts} critical alert(s) "
        f"and {warning_alerts} warning alert(s). "
        f"Leadership should prioritize suppliers with low risk scores, elevated PPM, or weak delivery performance."
    )

    return narrative