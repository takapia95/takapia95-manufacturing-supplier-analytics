USE supplier_quality_analytics;

CREATE INDEX idx_parts_supplier
ON Parts(SupplierID);

CREATE INDEX idx_po_supplier
ON PurchaseOrders(SupplierID);

CREATE INDEX idx_po_plant
ON PurchaseOrders(PlantID);

CREATE INDEX idx_delivery_date
ON Deliveries(DeliveryDate);

CREATE INDEX idx_inspection_date
ON Inspections(InspectionDate);

CREATE INDEX idx_defect_severity
ON Defects(Severity);

CREATE INDEX idx_car_status
ON CorrectiveActions(Status);

CREATE INDEX idx_audit_supplier
ON SupplierAudits(SupplierID);

CREATE INDEX idx_inventory_part
ON Inventory(PartID);

CREATE INDEX idx_monthly_kpi_supplier
ON MonthlySupplierKPIs(SupplierID);