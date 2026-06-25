USE supplier_quality_analytics;

CREATE TABLE IF NOT EXISTS Suppliers (
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

CREATE TABLE IF NOT EXISTS SupplierContacts (
    ContactID VARCHAR(10) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    ContactName VARCHAR(100) NOT NULL,
    JobTitle VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(25),
    CONSTRAINT fk_supplier_contacts_supplier
        FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
);

CREATE TABLE IF NOT EXISTS Plants (
    PlantID VARCHAR(10) PRIMARY KEY,
    PlantName VARCHAR(100) NOT NULL,
    City VARCHAR(50),
    State VARCHAR(50),
    Country VARCHAR(50),
    PlantType VARCHAR(50),
    OpeningDate DATE
);

CREATE TABLE IF NOT EXISTS ProductionLines (
    LineID VARCHAR(10) PRIMARY KEY,
    PlantID VARCHAR(10) NOT NULL,
    LineName VARCHAR(50) NOT NULL,
    Shift VARCHAR(20),
    CapacityPerDay INT,
    Status VARCHAR(20) DEFAULT 'Active',
    CONSTRAINT fk_production_lines_plant
        FOREIGN KEY (PlantID)
        REFERENCES Plants(PlantID)
);

CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    JobTitle VARCHAR(100),
    Department VARCHAR(50),
    PlantID VARCHAR(10),
    HireDate DATE,
    EmploymentStatus VARCHAR(20) DEFAULT 'Active',
    CONSTRAINT fk_employees_plant
        FOREIGN KEY (PlantID)
        REFERENCES Plants(PlantID)
);