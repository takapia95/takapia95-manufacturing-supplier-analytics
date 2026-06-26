/*
============================================================
 Manufacturing Supplier Intelligence Platform
 Master Tables
============================================================

Tables

1. Suppliers
2. SupplierContacts
3. Plants
4. ProductionLines
5. Employees

============================================================
*/

USE supplier_quality_analytics;

-- ==========================================================
-- Table: Suppliers
-- ==========================================================

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

    RiskLevel ENUM(
        'Low',
        'Medium',
        'High'
    ) DEFAULT 'Low',

    SupplierStatus ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    StartDate DATE,

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP

);

-- ==========================================================
-- Table: SupplierContacts
-- ==========================================================

CREATE TABLE SupplierContacts (

    ContactID VARCHAR(10) PRIMARY KEY,

    SupplierID VARCHAR(10) NOT NULL,

    ContactName VARCHAR(100) NOT NULL,

    JobTitle VARCHAR(100),

    Email VARCHAR(100),

    Phone VARCHAR(25),

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (SupplierID)

        REFERENCES Suppliers(SupplierID)

        ON DELETE CASCADE

);

-- ==========================================================
-- Table: Plants
-- ==========================================================

CREATE TABLE Plants (

    PlantID VARCHAR(10) PRIMARY KEY,

    PlantName VARCHAR(100) NOT NULL,

    City VARCHAR(50),

    State VARCHAR(50),

    Country VARCHAR(50),

    PlantType ENUM(

        'Assembly',

        'Engine',

        'Battery',

        'Distribution'

    ),

    OpeningDate DATE,

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================================================
-- Table: ProductionLines
-- ==========================================================

CREATE TABLE ProductionLines (

    LineID VARCHAR(10) PRIMARY KEY,

    PlantID VARCHAR(10) NOT NULL,

    LineName VARCHAR(50) NOT NULL,

    Shift ENUM(

        'Day',

        'Evening',

        'Night'

    ),

    CapacityPerDay INT,

    Status ENUM(

        'Active',

        'Maintenance',

        'Offline'

    ) DEFAULT 'Active',

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (PlantID)

        REFERENCES Plants(PlantID)

        ON DELETE CASCADE

);

-- ==========================================================
-- Table: Employees
-- ==========================================================

CREATE TABLE Employees (

    EmployeeID VARCHAR(10) PRIMARY KEY,

    FirstName VARCHAR(50) NOT NULL,

    LastName VARCHAR(50) NOT NULL,

    JobTitle VARCHAR(100),

    Department ENUM(

        'Quality',

        'Purchasing',

        'Production',

        'Engineering',

        'Logistics',

        'Management'

    ),

    PlantID VARCHAR(10),

    HireDate DATE,

    EmploymentStatus ENUM(

        'Active',

        'Leave',

        'Retired'

    ) DEFAULT 'Active',

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (PlantID)

        REFERENCES Plants(PlantID)

        ON DELETE SET NULL

);