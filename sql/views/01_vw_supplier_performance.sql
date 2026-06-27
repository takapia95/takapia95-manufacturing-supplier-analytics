USE supplier_quality_analytics;

DROP VIEW IF EXISTS vw_supplier_performance;

CREATE VIEW vw_supplier_performance AS
SELECT
    s.SupplierID,
    s.SupplierName,
    s.SupplierCategory,
    s.RiskLevel,
    s.SupplierStatus,

    COUNT(DISTINCT p.PartID) AS TotalPartsSupplied,
    COUNT(DISTINCT po.PO_ID) AS TotalPurchaseOrders,
    COUNT(DISTINCT d.DeliveryID) AS TotalDeliveries,

    ROUND(AVG(k.SupplierQualityScore), 2) AS AvgQualityScore,
    ROUND(AVG(k.OnTimeDeliveryRate), 2) AS AvgDeliveryScore,
    ROUND(AVG(k.SupplierQualityScore), 2) AS AvgOverallScore,
    ROUND(AVG(k.PPM), 2) AS AvgPPM,
    ROUND(AVG(k.OnTimeDeliveryRate), 2) AS AvgOnTimeDeliveryRate,

    CASE
        WHEN AVG(k.SupplierQualityScore) >= 90 THEN 'Excellent'
        WHEN AVG(k.SupplierQualityScore) >= 80 THEN 'Good'
        WHEN AVG(k.SupplierQualityScore) >= 70 THEN 'Watch'
        ELSE 'Critical'
    END AS SupplierPerformanceBand

FROM Suppliers s
LEFT JOIN Parts p
    ON s.SupplierID = p.SupplierID
LEFT JOIN PurchaseOrders po
    ON s.SupplierID = po.SupplierID
LEFT JOIN PurchaseOrderLines pol
    ON po.PO_ID = pol.PO_ID
LEFT JOIN Deliveries d
    ON pol.POLineID = d.POLineID
LEFT JOIN MonthlySupplierKPIs k
    ON s.SupplierID = k.SupplierID
GROUP BY
    s.SupplierID,
    s.SupplierName,
    s.SupplierCategory,
    s.RiskLevel,
    s.SupplierStatus;