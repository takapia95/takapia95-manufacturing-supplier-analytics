# -----------------------
# Executive Intelligence Rules
# -----------------------
# Centralized business thresholds for supplier quality,
# delivery performance, defects, inventory risk, and corrective actions.
#
# In a production BI environment, these thresholds would usually be
# reviewed with Supplier Quality, Operations, Procurement, and Finance.


# -----------------------
# Supplier Quality Rules
# -----------------------
QUALITY_EXCELLENT = 90
QUALITY_WARNING = 75


# -----------------------
# Defect / PPM Rules
# -----------------------
PPM_GOOD_MAX = 500
PPM_WARNING_MAX = 1500


# -----------------------
# Delivery Performance Rules
# -----------------------
OTD_EXCELLENT = 95
OTD_WARNING = 85


# -----------------------
# Risk Scoring Weights
# -----------------------
QUALITY_WEIGHT = 0.40
DELIVERY_WEIGHT = 0.30
PPM_WEIGHT = 0.20
CORRECTIVE_ACTION_WEIGHT = 0.10


# -----------------------
# Supplier Risk Rating Bands
# -----------------------
RISK_EXCELLENT = 90
RISK_GOOD = 80
RISK_WATCH = 70
RISK_HIGH = 60


def classify_quality(avg_quality_score):
    if avg_quality_score >= QUALITY_EXCELLENT:
        return "Strong"
    if avg_quality_score >= QUALITY_WARNING:
        return "Moderate"
    return "At Risk"


def classify_ppm(avg_ppm):
    if avg_ppm <= PPM_GOOD_MAX:
        return "Controlled"
    if avg_ppm <= PPM_WARNING_MAX:
        return "Elevated"
    return "High Risk"


def classify_delivery(avg_otd):
    if avg_otd >= OTD_EXCELLENT:
        return "Excellent"
    if avg_otd >= OTD_WARNING:
        return "Acceptable"
    return "Below Target"


def classify_risk_score(score):
    if score >= RISK_EXCELLENT:
        return "Excellent"
    if score >= RISK_GOOD:
        return "Good"
    if score >= RISK_WATCH:
        return "Watch"
    if score >= RISK_HIGH:
        return "High Risk"
    return "Critical"