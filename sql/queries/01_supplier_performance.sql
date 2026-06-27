USE supplier_quality_analytics;

-- =====================================================
-- 01_supplier_performance.sql
-- Manufacturing Supplier Intelligence Platform
-- Purpose: Supplier performance analytics for BI reporting
-- =====================================================


-- 1. Supplier Master Overview
SELECT
    SupplierID,
    SupplierName,
    SupplierType,
    City,
    State,
    Country,
    CertificationStatus,
    RiskLevel,
    Status
FROM Suppliers
ORDER BY SupplierName;


-- 2. Supplier Count by Risk Level
SELECT
    RiskLevel,
    COUNT(*) AS SupplierCount
FROM Suppliers
GROUP BY RiskLevel
ORDER BY SupplierCount DESC;


-- 3. Supplier Count by Certification Status
SELECT
    CertificationStatus,
    COUNT(*) AS SupplierCount
FROM Suppliers
GROUP BY CertificationStatus
ORDER BY SupplierCount DESC;


-- 4. Supplier Performance Ranking
SELECT
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel,
    ROUND(AVG(k.QualityScore), 2) AS AvgQualityScore,
    ROUND(AVG(k.DeliveryScore), 2) AS AvgDeliveryScore,
    ROUND(AVG(k.OverallScore), 2) AS AvgOverallScore,
    COUNT(k.KPIID) AS KPIRecords
FROM Suppliers s
JOIN MonthlySupplierKPIs k
    ON s.SupplierID = k.SupplierID
GROUP BY
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel
ORDER BY AvgOverallScore DESC;


-- 5. Lowest Performing Suppliers
SELECT
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel,
    ROUND(AVG(k.OverallScore), 2) AS AvgOverallScore,
    ROUND(AVG(k.QualityScore), 2) AS AvgQualityScore,
    ROUND(AVG(k.DeliveryScore), 2) AS AvgDeliveryScore
FROM Suppliers s
JOIN MonthlySupplierKPIs k
    ON s.SupplierID = k.SupplierID
GROUP BY
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel
ORDER BY AvgOverallScore ASC
LIMIT 10;


-- 6. Supplier Monthly Trend
SELECT
    s.SupplierName,
    k.KPIMonth,
    ROUND(k.QualityScore, 2) AS QualityScore,
    ROUND(k.DeliveryScore, 2) AS DeliveryScore,
    ROUND(k.OverallScore, 2) AS OverallScore,
    k.PPM,
    k.OnTimeDeliveryRate
FROM MonthlySupplierKPIs k
JOIN Suppliers s
    ON k.SupplierID = s.SupplierID
ORDER BY
    s.SupplierName,
    k.KPIMonth;


-- 7. High-Risk Suppliers with Poor Performance
SELECT
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel,
    ROUND(AVG(k.OverallScore), 2) AS AvgOverallScore,
    ROUND(AVG(k.PPM), 2) AS AvgPPM,
    ROUND(AVG(k.OnTimeDeliveryRate), 2) AS AvgOnTimeDeliveryRate
FROM Suppliers s
JOIN MonthlySupplierKPIs k
    ON s.SupplierID = k.SupplierID
WHERE s.RiskLevel = 'High'
GROUP BY
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel
HAVING AvgOverallScore < 80
ORDER BY AvgOverallScore ASC;


-- 8. Supplier Score Distribution
SELECT
    CASE
        WHEN OverallScore >= 90 THEN 'Excellent'
        WHEN OverallScore >= 80 THEN 'Good'
        WHEN OverallScore >= 70 THEN 'Watch'
        ELSE 'Critical'
    END AS PerformanceBand,
    COUNT(*) AS SupplierMonthRecords
FROM MonthlySupplierKPIs
GROUP BY PerformanceBand
ORDER BY SupplierMonthRecords DESC;


-- 9. Supplier Audit Performance
SELECT
    s.SupplierName,
    a.AuditDate,
    a.AuditType,
    a.AuditScore,
    a.AuditResult,
    a.AuditorName
FROM SupplierAudits a
JOIN Suppliers s
    ON a.SupplierID = s.SupplierID
ORDER BY
    a.AuditDate DESC,
    a.AuditScore ASC;


-- 10. Suppliers Requiring Management Attention
SELECT
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel,
    ROUND(AVG(k.OverallScore), 2) AS AvgOverallScore,
    ROUND(AVG(k.PPM), 2) AS AvgPPM,
    ROUND(AVG(k.OnTimeDeliveryRate), 2) AS AvgOTD,
    COUNT(DISTINCT ca.CorrectiveActionID) AS CorrectiveActionCount
FROM Suppliers s
LEFT JOIN MonthlySupplierKPIs k
    ON s.SupplierID = k.SupplierID
LEFT JOIN CorrectiveActions ca
    ON s.SupplierID = ca.SupplierID
GROUP BY
    s.SupplierID,
    s.SupplierName,
    s.RiskLevel
HAVING
    AvgOverallScore < 80
    OR AvgPPM > 500
    OR AvgOTD < 90
    OR CorrectiveActionCount >= 3
ORDER BY
    AvgOverallScore ASC,
    CorrectiveActionCount DESC;
