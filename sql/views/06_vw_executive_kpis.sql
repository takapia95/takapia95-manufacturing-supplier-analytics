CREATE OR REPLACE VIEW vw_executive_kpis AS
SELECT
    COUNT(DISTINCT sp.SupplierID) AS TotalSuppliers,
    ROUND(AVG(sp.AvgQualityScore), 2) AS AvgQualityScore,
    ROUND(AVG(sp.AvgPPM), 2) AS AvgPPM,
    ROUND(AVG(sp.AvgOnTimeDeliveryRate), 2) AS AvgOnTimeDeliveryRate,
    0 AS TotalScrapCost,
    ROUND((SELECT SUM(InventoryValue) FROM vw_inventory_summary), 2) AS TotalInventoryValue,
    (SELECT SUM(OpenActions) FROM vw_corrective_action_status) AS OpenCorrectiveActions,
    (SELECT SUM(LateDeliveries) FROM vw_delivery_summary) AS LateDeliveries
FROM vw_supplier_performance sp;