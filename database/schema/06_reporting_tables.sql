USE supplier_quality_analytics;

-- ==========================================================
-- Table: SupplierAudits
-- ==========================================================

CREATE TABLE SupplierAudits (

    AuditID VARCHAR(15) PRIMARY KEY,

    SupplierID VARCHAR(10) NOT NULL,

    AuditorID VARCHAR(10),

    AuditDate DATE NOT NULL,

    AuditScore DECIMAL(5,2),

    MajorFindings INT DEFAULT 0,

    MinorFindings INT DEFAULT 0,

    AuditResult ENUM(
        'Pass',
        'Conditional',
        'Fail'
    ),

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
        ON DELETE RESTRICT,

    FOREIGN KEY (AuditorID)
        REFERENCES Employees(EmployeeID)
        ON DELETE SET NULL
);

-- ==========================================================
-- Table: Inventory
-- ==========================================================

CREATE TABLE Inventory (

    InventoryID VARCHAR(15) PRIMARY KEY,

    PartID VARCHAR(10) NOT NULL,

    PlantID VARCHAR(10) NOT NULL,

    CurrentStock INT DEFAULT 0,

    SafetyStock INT DEFAULT 0,

    ReorderLevel INT DEFAULT 0,

    LastUpdated DATE,

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (PartID)
        REFERENCES Parts(PartID)
        ON DELETE RESTRICT,

    FOREIGN KEY (PlantID)
        REFERENCES Plants(PlantID)
        ON DELETE RESTRICT
);

-- ==========================================================
-- Table: MonthlySupplierKPIs
-- ==========================================================

CREATE TABLE MonthlySupplierKPIs (

    KPI_ID VARCHAR(15) PRIMARY KEY,

    SupplierID VARCHAR(10) NOT NULL,

    Month DATE NOT NULL,

    TotalReceived INT DEFAULT 0,

    TotalDefective INT DEFAULT 0,

    PPM DECIMAL(12,2),

    OnTimeDeliveryRate DECIMAL(5,2),

    AverageInspectionScore DECIMAL(5,2),

    ScrapCost DECIMAL(12,2),

    OpenCARCount INT DEFAULT 0,

    SupplierQualityScore DECIMAL(5,2),

    RiskLevel ENUM(
        'Low',
        'Medium',
        'High',
        'Critical'
    ),

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
        ON DELETE CASCADE
);