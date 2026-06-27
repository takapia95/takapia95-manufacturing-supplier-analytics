USE supplier_quality_analytics;

DROP VIEW IF EXISTS vw_monthly_supplier_trends;

CREATE VIEW vw_monthly_supplier_trends AS
SELECT
    SupplierID,
    Month,
    TotalReceived,
    TotalDefective,
    PPM,
    OnTimeDeliveryRate,
    AverageInspectionScore,
    ScrapCost,
    OpenCARCount,
    SupplierQualityScore,
    RiskLevel
FROM MonthlySupplierKPIs;