USE supplier_quality_analytics;

CREATE TABLE PartCategories (
    PartCategoryID VARCHAR(10) PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Parts (
    PartID VARCHAR(10) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    PartCategoryID VARCHAR(10) NOT NULL,
    PartName VARCHAR(100) NOT NULL,
    Material VARCHAR(50),
    UnitCost DECIMAL(10,2),
    CriticalPart BOOLEAN DEFAULT FALSE,
    PartStatus ENUM('Active', 'Inactive', 'Obsolete') DEFAULT 'Active',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
        ON DELETE CASCADE,

    FOREIGN KEY (PartCategoryID)
        REFERENCES PartCategories(PartCategoryID)
        ON DELETE RESTRICT
);