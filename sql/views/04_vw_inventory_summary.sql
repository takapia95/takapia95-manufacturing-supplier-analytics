CREATE OR REPLACE VIEW vw_inventory_summary AS
SELECT
    s.SupplierID,
    s.SupplierName,
    p.PartID,
    p.PartName,
    p.UnitCost,
    i.CurrentStock AS StockLevel,
    i.SafetyStock,
    i.ReorderLevel,
    (i.CurrentStock * p.UnitCost) AS InventoryValue,
    CASE
        WHEN i.CurrentStock <= i.ReorderLevel THEN 1
        ELSE 0
    END AS LowStockFlag
FROM Inventory i
JOIN Parts p
    ON i.PartID = p.PartID
JOIN Suppliers s
    ON p.SupplierID = s.SupplierID;