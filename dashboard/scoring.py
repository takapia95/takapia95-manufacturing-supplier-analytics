import pandas as pd

from dashboard.rules import (
    QUALITY_WEIGHT,
    DELIVERY_WEIGHT,
    PPM_WEIGHT,
    classify_risk_score,
)


def _normalize_ppm(ppm):
    """
    Convert PPM into a 0-100 score.
    Lower PPM is better.
    """
    if pd.isna(ppm):
        return 0

    score = 100 - (ppm / 20)
    return max(0, min(100, score))


def calculate_supplier_risk_scores(supplier_df):
    df = supplier_df.copy()

    required_columns = [
        "AvgQualityScore",
        "AvgOnTimeDeliveryRate",
        "AvgPPM",
    ]

    for col in required_columns:
        if col not in df.columns:
            df["SupplierRiskScore"] = None
            df["SupplierRiskRating"] = "Unavailable"
            return df

    df["PPMScore"] = df["AvgPPM"].apply(_normalize_ppm)

    df["SupplierRiskScore"] = (
        df["AvgQualityScore"] * QUALITY_WEIGHT
        + df["AvgOnTimeDeliveryRate"] * DELIVERY_WEIGHT
        + df["PPMScore"] * PPM_WEIGHT
    )

    df["SupplierRiskRating"] = df["SupplierRiskScore"].apply(classify_risk_score)

    return df