CREATE OR REPLACE VIEW vw_delivery_summary AS
SELECT
    s.SupplierID,
    s.SupplierName,
    COUNT(d.DeliveryID) AS TotalDeliveries,
    SUM(CASE WHEN d.OnTimeFlag = 0 THEN 1 ELSE 0 END) AS LateDeliveries,
    ROUND(
        SUM(CASE WHEN d.OnTimeFlag = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(d.DeliveryID), 0) * 100,
        2
    ) AS OnTimeDeliveryRate
FROM Suppliers s
LEFT JOIN PurchaseOrders po
    ON s.SupplierID = po.SupplierID
LEFT JOIN PurchaseOrderLines pol
    ON po.PO_ID = pol.PO_ID
LEFT JOIN Deliveries d
    ON pol.POLineID = d.POLineID
GROUP BY
    s.SupplierID,
    s.SupplierName;