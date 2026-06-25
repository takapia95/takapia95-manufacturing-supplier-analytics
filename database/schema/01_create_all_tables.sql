
CREATE DATABASE IF NOT EXISTS supplier_quality_analytics;
USE supplier_quality_analytics;

DROP TABLE IF EXISTS MonthlySupplierKPIs;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS SupplierAudits;
DROP TABLE IF EXISTS CorrectiveActions;
DROP TABLE IF EXISTS Defects;
DROP TABLE IF EXISTS RootCauses;
DROP TABLE IF EXISTS DefectCategories;
DROP TABLE IF EXISTS Inspections;
DROP TABLE IF EXISTS Deliveries;
DROP TABLE IF EXISTS PurchaseOrderLines;
DROP TABLE IF EXISTS PurchaseOrders;
DROP TABLE IF EXISTS Parts;
DROP TABLE IF EXISTS PartCategories;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS ProductionLines;
DROP TABLE IF EXISTS Plants;
DROP TABLE IF EXISTS SupplierContacts;
DROP TABLE IF EXISTS Suppliers;

CREATE TABLE Suppliers (
    SupplierID VARCHAR(10) PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    SupplierCategory VARCHAR(50),
    Country VARCHAR(50),
    State VARCHAR(50),
    City VARCHAR(50),
    ISO9001Certified BOOLEAN DEFAULT FALSE,
    IATF16949Certified BOOLEAN DEFAULT FALSE,
    PreferredSupplier BOOLEAN DEFAULT FALSE,
    RiskLevel VARCHAR(20),
    SupplierStatus VARCHAR(20) DEFAULT 'Active',
    StartDate DATE
);

CREATE TABLE SupplierContacts (
    ContactID VARCHAR(10) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    ContactName VARCHAR(100) NOT NULL,
    JobTitle VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(25),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

CREATE TABLE Plants (
    PlantID VARCHAR(10) PRIMARY KEY,
    PlantName VARCHAR(100) NOT NULL,
    City VARCHAR(50),
    State VARCHAR(50),
    Country VARCHAR(50),
    PlantType VARCHAR(50),
    OpeningDate DATE
);

CREATE TABLE ProductionLines (
    LineID VARCHAR(10) PRIMARY KEY,
    PlantID VARCHAR(10) NOT NULL,
    LineName VARCHAR(50) NOT NULL,
    Shift VARCHAR(20),
    CapacityPerDay INT,
    Status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (PlantID) REFERENCES Plants(PlantID)
);

CREATE TABLE Employees (
    EmployeeID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    JobTitle VARCHAR(100),
    Department VARCHAR(50),
    PlantID VARCHAR(10),
    HireDate DATE,
    EmploymentStatus VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (PlantID) REFERENCES Plants(PlantID)
);

CREATE TABLE PartCategories (
    PartCategoryID VARCHAR(10) PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL,
    Description TEXT
);

CREATE TABLE Parts (
    PartID VARCHAR(10) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    PartCategoryID VARCHAR(10) NOT NULL,
    PartName VARCHAR(100) NOT NULL,
    Material VARCHAR(50),
    UnitCost DECIMAL(10,2),
    CriticalPart BOOLEAN DEFAULT FALSE,
    PartStatus VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
    FOREIGN KEY (PartCategoryID) REFERENCES PartCategories(PartCategoryID)
);

CREATE TABLE PurchaseOrders (
    PO_ID VARCHAR(15) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    PlantID VARCHAR(10) NOT NULL,
    OrderDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    POStatus VARCHAR(20) DEFAULT 'Open',
    TotalAmount DECIMAL(12,2),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
    FOREIGN KEY (PlantID) REFERENCES Plants(PlantID)
);

CREATE TABLE PurchaseOrderLines (
    POLineID VARCHAR(15) PRIMARY KEY,
    PO_ID VARCHAR(15) NOT NULL,
    PartID VARCHAR(10) NOT NULL,
    OrderedQuantity INT NOT NULL,
    UnitCost DECIMAL(10,2),
    LineTotal DECIMAL(12,2),
    FOREIGN KEY (PO_ID) REFERENCES PurchaseOrders(PO_ID),
    FOREIGN KEY (PartID) REFERENCES Parts(PartID)
);

CREATE TABLE Deliveries (
    DeliveryID VARCHAR(15) PRIMARY KEY,
    POLineID VARCHAR(15) NOT NULL,
    DeliveryDate DATE NOT NULL,
    ReceivedQuantity INT NOT NULL,
    RejectedQuantity INT DEFAULT 0,
    DelayDays INT DEFAULT 0,
    OnTimeFlag BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (POLineID) REFERENCES PurchaseOrderLines(POLineID)
);

CREATE TABLE Inspections (
    InspectionID VARCHAR(15) PRIMARY KEY,
    DeliveryID VARCHAR(15) NOT NULL,
    InspectorID VARCHAR(10),
    InspectionDate DATE NOT NULL,
    InspectedQuantity INT NOT NULL,
    PassedQuantity INT,
    FailedQuantity INT,
    InspectionScore DECIMAL(5,2),
    InspectionResult VARCHAR(30),
    FOREIGN KEY (DeliveryID) REFERENCES Deliveries(DeliveryID),
    FOREIGN KEY (InspectorID) REFERENCES Employees(EmployeeID)
);

CREATE TABLE DefectCategories (
    DefectCategoryID VARCHAR(10) PRIMARY KEY,
    DefectName VARCHAR(100) NOT NULL,
    Description TEXT
);

CREATE TABLE RootCauses (
    RootCauseID VARCHAR(10) PRIMARY KEY,
    RootCauseName VARCHAR(100) NOT NULL,
    Description TEXT
);

CREATE TABLE Defects (
    DefectID VARCHAR(15) PRIMARY KEY,
    InspectionID VARCHAR(15) NOT NULL,
    DefectCategoryID VARCHAR(10) NOT NULL,
    RootCauseID VARCHAR(10),
    DefectQuantity INT NOT NULL,
    Severity VARCHAR(20),
    ScrapQuantity INT DEFAULT 0,
    ReworkQuantity INT DEFAULT 0,
    DefectCost DECIMAL(12,2),
    FOREIGN KEY (InspectionID) REFERENCES Inspections(InspectionID),
    FOREIGN KEY (DefectCategoryID) REFERENCES DefectCategories(DefectCategoryID),
    FOREIGN KEY (RootCauseID) REFERENCES RootCauses(RootCauseID)
);

CREATE TABLE CorrectiveActions (
    CAR_ID VARCHAR(15) PRIMARY KEY,
    DefectID VARCHAR(15) NOT NULL,
    SupplierID VARCHAR(10) NOT NULL,
    OpenDate DATE NOT NULL,
    DueDate DATE,
    CloseDate DATE,
    Status VARCHAR(30) DEFAULT 'Open',
    OwnerID VARCHAR(10),
    ActionDescription TEXT,
    VerificationStatus VARCHAR(30),
    FOREIGN KEY (DefectID) REFERENCES Defects(DefectID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
    FOREIGN KEY (OwnerID) REFERENCES Employees(EmployeeID)
);

CREATE TABLE SupplierAudits (
    AuditID VARCHAR(15) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    AuditorID VARCHAR(10),
    AuditDate DATE NOT NULL,
    AuditScore DECIMAL(5,2),
    MajorFindings INT DEFAULT 0,
    MinorFindings INT DEFAULT 0,
    AuditResult VARCHAR(30),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
    FOREIGN KEY (AuditorID) REFERENCES Employees(EmployeeID)
);

CREATE TABLE Inventory (
    InventoryID VARCHAR(15) PRIMARY KEY,
    PartID VARCHAR(10) NOT NULL,
    PlantID VARCHAR(10) NOT NULL,
    CurrentStock INT DEFAULT 0,
    SafetyStock INT DEFAULT 0,
    ReorderLevel INT DEFAULT 0,
    LastUpdated DATE,
    FOREIGN KEY (PartID) REFERENCES Parts(PartID),
    FOREIGN KEY (PlantID) REFERENCES Plants(PlantID)
);

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
    RiskLevel VARCHAR(20),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);
```
