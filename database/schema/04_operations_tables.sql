USE supplier_quality_analytics;

CREATE TABLE Deliveries (
    DeliveryID VARCHAR(15) PRIMARY KEY,
    POLineID VARCHAR(15) NOT NULL,
    DeliveryDate DATE NOT NULL,
    ReceivedQuantity INT NOT NULL,
    RejectedQuantity INT DEFAULT 0,
    DelayDays INT DEFAULT 0,
    OnTimeFlag BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (POLineID)
        REFERENCES PurchaseOrderLines(POLineID)
        ON DELETE CASCADE
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
    InspectionResult ENUM('Pass', 'Minor Issue', 'Fail') DEFAULT 'Pass',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (DeliveryID)
        REFERENCES Deliveries(DeliveryID)
        ON DELETE CASCADE,

    FOREIGN KEY (InspectorID)
        REFERENCES Employees(EmployeeID)
        ON DELETE SET NULL
);