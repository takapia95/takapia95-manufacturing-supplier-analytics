import pandas as pd
from dashboard.rules import (
    QUALITY_EXCELLENT,
    QUALITY_WARNING,
    PPM_GOOD_MAX,
    PPM_WARNING_MAX,
    OTD_EXCELLENT,
    OTD_WARNING,
)

def _has_column(df, column):
    return df is not None and not df.empty and column in df.columns


def _format_number(value, decimals=2):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"


def _format_percent(value, decimals=2):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}%"


def generate_executive_summary(
    kpi_df,
    supplier_df,
    delivery_df,
    inventory_df,
    ca_df
):
    insights = []

    # -----------------------
    # Supplier Quality Health
    # -----------------------
    if _has_column(supplier_df, "AvgQualityScore"):
        avg_quality = supplier_df["AvgQualityScore"].mean()

        if avg_quality >= QUALITY_EXCELLENT:
            insights.append(
                f"Supplier quality health is strong, with an average quality score of "
                f"{_format_number(avg_quality)}. The supplier base appears stable from a quality standpoint."
            )
        elif avg_quality >= QUALITY_WARNING:
            insights.append(
                f"Supplier quality health is moderate, with an average quality score of "
                f"{_format_number(avg_quality)}. Leadership should monitor suppliers trending below target."
            )
        else:
            insights.append(
                f"Supplier quality health is at risk, with an average quality score of "
                f"{_format_number(avg_quality)}. Immediate supplier quality review is recommended."
            )

    # -----------------------
    # Defect / PPM Assessment
    # -----------------------
    if _has_column(supplier_df, "AvgPPM"):
        avg_ppm = supplier_df["AvgPPM"].mean()

        if avg_ppm <= PPM_GOOD_MAX:
            insights.append(
                f"Defect performance is controlled, with an average PPM of "
                f"{_format_number(avg_ppm)} across suppliers."
            )
        elif avg_ppm <= PPM_WARNING_MAX:
            insights.append(
                f"Defect performance is elevated, with an average PPM of "
                f"{_format_number(avg_ppm)}. Supplier process capability should be reviewed."
            )
        else:
            insights.append(
                f"Defect performance is high-risk, with an average PPM of "
                f"{_format_number(avg_ppm)}. Containment, root cause analysis, and corrective action should be prioritized."
            )

    # -----------------------
    # Delivery Performance
    # -----------------------
    if _has_column(supplier_df, "AvgOnTimeDeliveryRate"):
        avg_otd = supplier_df["AvgOnTimeDeliveryRate"].mean()

        if avg_otd >= 95:
            insights.append(
                f"Delivery performance is excellent, with an average on-time delivery rate of "
                f"{_format_percent(avg_otd)}."
            )
        elif avg_otd >= 85:
            insights.append(
                f"Delivery performance is acceptable but should be monitored, with an average on-time delivery rate of "
                f"{_format_percent(avg_otd)}."
            )
        else:
            insights.append(
                f"Delivery performance is below target, with an average on-time delivery rate of "
                f"{_format_percent(avg_otd)}. This may create production schedule risk."
            )

    # -----------------------
    # Supplier Risk Bands
    # -----------------------
    if _has_column(supplier_df, "SupplierPerformanceBand"):
        risk_counts = supplier_df["SupplierPerformanceBand"].value_counts()

        high_risk_count = 0
        for label in risk_counts.index:
            if "risk" in str(label).lower() or "poor" in str(label).lower():
                high_risk_count += risk_counts[label]

        if high_risk_count > 0:
            insights.append(
                f"{int(high_risk_count)} supplier(s) are currently classified in a lower performance or risk band. "
                f"These suppliers should be reviewed for quality, delivery, or process stability concerns."
            )
        else:
            insights.append(
                "No suppliers are currently concentrated in a major risk band based on the supplier performance classification."
            )

    # -----------------------
    # Inventory Risk
    # -----------------------
    if inventory_df is not None and not inventory_df.empty:
        inventory_risk_found = False

        for col in inventory_df.columns:
            if "risk" in col.lower() or "status" in col.lower():
                risky_rows = inventory_df[
                    inventory_df[col]
                    .astype(str)
                    .str.contains("high|critical|low|shortage", case=False, na=False)
                ]

                if len(risky_rows) > 0:
                    insights.append(
                        f"Inventory risk is present in {len(risky_rows)} record(s). "
                        f"Leadership should validate safety stock, reorder points, and supplier lead times."
                    )
                    inventory_risk_found = True
                    break

        if not inventory_risk_found:
            insights.append(
                "Inventory position appears stable based on the current inventory summary view."
            )

    # -----------------------
    # Corrective Action Status
    # -----------------------
    if ca_df is not None and not ca_df.empty:
        open_action_found = False

        for col in ca_df.columns:
            if "open" in col.lower() or "pending" in col.lower():
                try:
                    open_total = ca_df[col].sum()

                    if open_total > 0:
                        insights.append(
                            f"There are {int(open_total)} open or pending corrective action(s). "
                            f"Supplier follow-up should remain a management priority."
                        )
                    else:
                        insights.append(
                            "Corrective action status is healthy, with no open or pending actions reported."
                        )

                    open_action_found = True
                    break
                except TypeError:
                    continue

        if not open_action_found:
            insights.append(
                "Corrective action data is available, but no open-action field was identified for automated summary."
            )

    return insights


def generate_recommendations(
    kpi_df,
    supplier_df,
    delivery_df,
    inventory_df,
    ca_df
):
    recommendations = []

    # Supplier quality recommendation
    if _has_column(supplier_df, "AvgQualityScore"):
        avg_quality = supplier_df["AvgQualityScore"].mean()

        if avg_quality < 75:
            recommendations.append(
                "Schedule immediate supplier quality review meetings for suppliers below acceptable quality thresholds."
            )
        elif avg_quality < 90:
            recommendations.append(
                "Monitor suppliers with declining quality scores and review process capability before issues impact production."
            )
        else:
            recommendations.append(
                "Maintain the current supplier governance cadence while continuing quality trend monitoring."
            )

    # Defect recommendation
    if _has_column(supplier_df, "AvgPPM"):
        avg_ppm = supplier_df["AvgPPM"].mean()

        if avg_ppm > PPM_WARNING_MAX:
            recommendations.append(
                "Prioritize root cause analysis and containment actions for suppliers contributing to elevated PPM."
            )
        elif avg_ppm > PPM_GOOD_MAX:
            recommendations.append(
                "Review supplier defect trends and identify recurring part or process issues."
            )

    # Delivery recommendation
    if _has_column(supplier_df, "AvgOnTimeDeliveryRate"):
        avg_otd = supplier_df["AvgOnTimeDeliveryRate"].mean()

        if avg_otd < 85:
            recommendations.append(
                "Escalate late-delivery suppliers and validate whether production schedules are exposed to material shortage risk."
            )
        elif avg_otd < 95:
            recommendations.append(
                "Review delivery performance by supplier and part category to prevent schedule disruption."
            )

    # Inventory recommendation
    if inventory_df is not None and not inventory_df.empty:
        recommendations.append(
            "Cross-check inventory risk with supplier delivery performance to identify parts vulnerable to shortage or expedited freight cost."
        )

    # Corrective action recommendation
    if ca_df is not None and not ca_df.empty:
        recommendations.append(
            "Track aging corrective actions weekly and review overdue items during supplier performance meetings."
        )

    if not recommendations:
        recommendations.append(
            "Continue monitoring supplier performance KPIs and refresh executive insights as new data is loaded."
        )

    return recommendations