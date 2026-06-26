USE supplier_quality_analytics;

CREATE VIEW vw_supplier_summary AS

SELECT

    SupplierID,

    SupplierName,

    SupplierCategory,

    RiskLevel,

    SupplierStatus

FROM Suppliers;