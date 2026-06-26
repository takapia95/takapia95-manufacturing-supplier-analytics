USE supplier_quality_analytics;

CREATE TABLE DefectCategories (
    DefectCategoryID VARCHAR(10) PRIMARY KEY,
    DefectName VARCHAR(100) NOT NULL,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE RootCauses (
    RootCauseID VARCHAR(10) PRIMARY KEY,
    RootCauseName VARCHAR(100) NOT NULL,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Defects (
    DefectID VARCHAR(15) PRIMARY KEY,
    InspectionID VARCHAR(15) NOT NULL,
    DefectCategoryID VARCHAR(10) NOT NULL,
    RootCauseID VARCHAR(10),
    DefectQuantity INT NOT NULL,
    Severity ENUM('Minor', 'Major', 'Critical') DEFAULT 'Minor',
    ScrapQuantity INT DEFAULT 0,
    ReworkQuantity INT DEFAULT 0,
    DefectCost DECIMAL(12,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (InspectionID)
        REFERENCES Inspections(InspectionID)
        ON DELETE CASCADE,

    FOREIGN KEY (DefectCategoryID)
        REFERENCES DefectCategories(DefectCategoryID)
        ON DELETE RESTRICT,

    FOREIGN KEY (RootCauseID)
        REFERENCES RootCauses(RootCauseID)
        ON DELETE SET NULL
);

CREATE TABLE CorrectiveActions (
    CAR_ID VARCHAR(15) PRIMARY KEY,
    DefectID VARCHAR(15) NOT NULL,
    SupplierID VARCHAR(10) NOT NULL,
    OpenDate DATE NOT NULL,
    DueDate DATE,
    CloseDate DATE,
    Status ENUM('Open', 'In Progress', 'Closed', 'Overdue') DEFAULT 'Open',
    OwnerID VARCHAR(10),
    ActionDescription TEXT,
    VerificationStatus ENUM('Pending', 'Verified', 'Rejected') DEFAULT 'Pending',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (DefectID)
        REFERENCES Defects(DefectID)
        ON DELETE CASCADE,

    FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
        ON DELETE RESTRICT,

    FOREIGN KEY (OwnerID)
        REFERENCES Employees(EmployeeID)
        ON DELETE SET NULL
);