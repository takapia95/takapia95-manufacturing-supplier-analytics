USE supplier_quality_analytics;

DELIMITER $$

CREATE PROCEDURE GetSupplierSummary()

BEGIN

    SELECT *

    FROM vw_supplier_summary;

END $$

DELIMITER ;