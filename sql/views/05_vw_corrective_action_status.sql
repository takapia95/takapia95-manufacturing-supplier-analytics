CREATE OR REPLACE VIEW vw_corrective_action_status AS
SELECT
    s.SupplierID,
    s.SupplierName,
    COUNT(ca.CAR_ID) AS TotalActions,
    SUM(CASE WHEN ca.Status IN ('Open', 'In Progress', 'Overdue') THEN 1 ELSE 0 END) AS OpenActions,
    SUM(CASE WHEN ca.Status = 'Closed' THEN 1 ELSE 0 END) AS ClosedActions,
    SUM(CASE WHEN ca.Status = 'Overdue' THEN 1 ELSE 0 END) AS OverdueActions
FROM Suppliers s
LEFT JOIN CorrectiveActions ca
    ON s.SupplierID = ca.SupplierID
GROUP BY
    s.SupplierID,
    s.SupplierName;