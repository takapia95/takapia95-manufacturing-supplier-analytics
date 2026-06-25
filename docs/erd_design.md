# ERD Design

## Manufacturing Supplier Intelligence Platform

---

# Purpose

This document defines the Entity Relationship Diagram (ERD) for the Manufacturing Supplier Intelligence Platform.

The ERD shows how supplier, part, purchasing, delivery, inspection, defect, corrective action, audit, inventory, and KPI data connect inside the database.

---

# Main Business Flow

```text
Supplier
   ↓
Part
   ↓
Purchase Order
   ↓
Purchase Order Line
   ↓
Delivery
   ↓
Inspection
   ↓
Defect
   ↓
Corrective Action
```

---

# Mermaid ERD

```mermaid
erDiagram

    SUPPLIERS {
        varchar SupplierID PK
        varchar SupplierName
        varchar SupplierCategory
        varchar Country
        varchar State
        varchar City
        boolean ISO9001Certified
        boolean IATF16949Certified
        boolean PreferredSupplier
        varchar RiskLevel
        varchar SupplierStatus
        date StartDate
    }

    SUPPLIER_CONTACTS {
        varchar ContactID PK
        varchar SupplierID FK
        varchar ContactName
        varchar JobTitle
        varchar Email
        varchar Phone
    }

    PLANTS {
        varchar PlantID PK
        varchar PlantName
        varchar City
        varchar State
        varchar Country
        varchar PlantType
        date OpeningDate
    }

    PRODUCTION_LINES {
        varchar LineID PK
        varchar PlantID FK
        varchar LineName
        varchar Shift
        int CapacityPerDay
        varchar Status
    }

    EMPLOYEES {
        varchar EmployeeID PK
        varchar FirstName
        varchar LastName
        varchar JobTitle
        varchar Department
        varchar PlantID FK
        date HireDate
        varchar EmploymentStatus
    }

    PART_CATEGORIES {
        varchar PartCategoryID PK
        varchar CategoryName
        text Description
    }

    PARTS {
        varchar PartID PK
        varchar SupplierID FK
        varchar PartCategoryID FK
        varchar PartName
        varchar Material
        decimal UnitCost
        boolean CriticalPart
        varchar PartStatus
    }

    PURCHASE_ORDERS {
        varchar PO_ID PK
        varchar SupplierID FK
        varchar PlantID FK
        date OrderDate
        date DueDate
        varchar POStatus
        decimal TotalAmount
    }

    PURCHASE_ORDER_LINES {
        varchar POLineID PK
        varchar PO_ID FK
        varchar PartID FK
        int OrderedQuantity
        decimal UnitCost
        decimal LineTotal
    }

    DELIVERIES {
        varchar DeliveryID PK
        varchar POLineID FK
        date DeliveryDate
        int ReceivedQuantity
        int RejectedQuantity
        int DelayDays
        boolean OnTimeFlag
    }

    INSPECTIONS {
        varchar InspectionID PK
        varchar DeliveryID FK
        varchar InspectorID FK
        date InspectionDate
        int InspectedQuantity
        int PassedQuantity
        int FailedQuantity
        decimal InspectionScore
        varchar InspectionResult
    }

    DEFECT_CATEGORIES {
        varchar DefectCategoryID PK
        varchar DefectName
        text Description
    }

    ROOT_CAUSES {
        varchar RootCauseID PK
        varchar RootCauseName
        text Description
    }

    DEFECTS {
        varchar DefectID PK
        varchar InspectionID FK
        varchar DefectCategoryID FK
        varchar RootCauseID FK
        int DefectQuantity
        varchar Severity
        int ScrapQuantity
        int ReworkQuantity
        decimal DefectCost
    }

    CORRECTIVE_ACTIONS {
        varchar CAR_ID PK
        varchar DefectID FK
        varchar SupplierID FK
        date OpenDate
        date DueDate
        date CloseDate
        varchar Status
        varchar OwnerID FK
        text ActionDescription
        varchar VerificationStatus
    }

    SUPPLIER_AUDITS {
        varchar AuditID PK
        varchar SupplierID FK
        varchar AuditorID FK
        date AuditDate
        decimal AuditScore
        int MajorFindings
        int MinorFindings
        varchar AuditResult
    }

    INVENTORY {
        varchar InventoryID PK
        varchar PartID FK
        varchar PlantID FK
        int CurrentStock
        int SafetyStock
        int ReorderLevel
        date LastUpdated
    }

    MONTHLY_SUPPLIER_KPIS {
        varchar KPI_ID PK
        varchar SupplierID FK
        date Month
        int TotalReceived
        int TotalDefective
        decimal PPM
        decimal OnTimeDeliveryRate
        decimal AverageInspectionScore
        decimal ScrapCost
        int OpenCARCount
        decimal SupplierQualityScore
        varchar RiskLevel
    }

    SUPPLIERS ||--o{ SUPPLIER_CONTACTS : has
    SUPPLIERS ||--o{ PARTS : supplies
    SUPPLIERS ||--o{ PURCHASE_ORDERS : receives
    SUPPLIERS ||--o{ SUPPLIER_AUDITS : audited
    SUPPLIERS ||--o{ CORRECTIVE_ACTIONS : responsible_for
    SUPPLIERS ||--o{ MONTHLY_SUPPLIER_KPIS : measured_by

    PART_CATEGORIES ||--o{ PARTS : classifies

    PLANTS ||--o{ PRODUCTION_LINES : contains
    PLANTS ||--o{ EMPLOYEES : employs
    PLANTS ||--o{ PURCHASE_ORDERS : receives
    PLANTS ||--o{ INVENTORY : stores

    PARTS ||--o{ PURCHASE_ORDER_LINES : ordered_in
    PARTS ||--o{ INVENTORY : stocked_as

    PURCHASE_ORDERS ||--o{ PURCHASE_ORDER_LINES : contains
    PURCHASE_ORDER_LINES ||--o{ DELIVERIES : fulfilled_by

    DELIVERIES ||--o{ INSPECTIONS : inspected_by
    INSPECTIONS ||--o{ DEFECTS : identifies

    DEFECT_CATEGORIES ||--o{ DEFECTS : categorizes
    ROOT_CAUSES ||--o{ DEFECTS : explains
    DEFECTS ||--o{ CORRECTIVE_ACTIONS : triggers

    EMPLOYEES ||--o{ INSPECTIONS : performs
    EMPLOYEES ||--o{ SUPPLIER_AUDITS : audits
    EMPLOYEES ||--o{ CORRECTIVE_ACTIONS : owns
```

---

# Relationship Summary

| Parent Table       | Child Table         | Relationship                                       |
| ------------------ | ------------------- | -------------------------------------------------- |
| Suppliers          | SupplierContacts    | One supplier has many contacts                     |
| Suppliers          | Parts               | One supplier provides many parts                   |
| Suppliers          | PurchaseOrders      | One supplier receives many purchase orders         |
| Suppliers          | SupplierAudits      | One supplier has many audits                       |
| Suppliers          | CorrectiveActions   | One supplier may have many corrective actions      |
| Suppliers          | MonthlySupplierKPIs | One supplier has monthly KPI records               |
| Plants             | ProductionLines     | One plant has many production lines                |
| Plants             | Employees           | One plant has many employees                       |
| Plants             | PurchaseOrders      | One plant receives many purchase orders            |
| Plants             | Inventory           | One plant stores many inventory records            |
| PartCategories     | Parts               | One category contains many parts                   |
| Parts              | PurchaseOrderLines  | One part appears on many PO lines                  |
| Parts              | Inventory           | One part may exist in multiple inventory records   |
| PurchaseOrders     | PurchaseOrderLines  | One purchase order has many lines                  |
| PurchaseOrderLines | Deliveries          | One PO line may have many deliveries               |
| Deliveries         | Inspections         | One delivery may have many inspections             |
| Inspections        | Defects             | One inspection may identify many defects           |
| DefectCategories   | Defects             | One defect category appears in many defect records |
| RootCauses         | Defects             | One root cause appears in many defect records      |
| Defects            | CorrectiveActions   | One defect may trigger corrective actions          |
| Employees          | Inspections         | One employee may perform many inspections          |
| Employees          | SupplierAudits      | One employee may perform many audits               |
| Employees          | CorrectiveActions   | One employee may own many corrective actions       |

---

# Design Notes

* The design follows a normalized relational model.
* Operational records flow from purchase orders to inspections and defects.
* Supplier KPIs are stored separately in `MonthlySupplierKPIs` to support faster reporting.
* Corrective actions connect both supplier responsibility and defect history.
* Employees are used as inspectors, auditors, and corrective action owners.
* Inventory connects parts to plant-level stock levels.
