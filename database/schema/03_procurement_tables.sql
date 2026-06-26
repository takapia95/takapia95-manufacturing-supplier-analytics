USE supplier_quality_analytics;

CREATE TABLE PurchaseOrders (
    PO_ID VARCHAR(15) PRIMARY KEY,
    SupplierID VARCHAR(10) NOT NULL,
    PlantID VARCHAR(10) NOT NULL,
    OrderDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    POStatus ENUM('Open', 'Closed', 'Delayed', 'Cancelled') DEFAULT 'Open',
    TotalAmount DECIMAL(12,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (SupplierID)
        REFERENCES Suppliers(SupplierID)
        ON DELETE RESTRICT,

    FOREIGN KEY (PlantID)
        REFERENCES Plants(PlantID)
        ON DELETE RESTRICT
);

CREATE TABLE PurchaseOrderLines (
    POLineID VARCHAR(15) PRIMARY KEY,
    PO_ID VARCHAR(15) NOT NULL,
    PartID VARCHAR(10) NOT NULL,
    OrderedQuantity INT NOT NULL,
    UnitCost DECIMAL(10,2),
    LineTotal DECIMAL(12,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (PO_ID)
        REFERENCES PurchaseOrders(PO_ID)
        ON DELETE CASCADE,

    FOREIGN KEY (PartID)
        REFERENCES Parts(PartID)
        ON DELETE RESTRICT
);