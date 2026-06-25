# Data Dictionary

## Manufacturing Supplier Intelligence Platform

---

# Overview

This document defines the database structure for the Manufacturing Supplier Intelligence Platform.

The database is designed to simulate an enterprise Supplier Quality Management System (SQMS) commonly used in the automotive manufacturing industry.

Each table includes:

* Business Purpose
* Primary Key
* Foreign Keys
* Column Definitions
* Data Types
* Business Descriptions
* Estimated Record Count

The database follows Third Normal Form (3NF) to minimize redundancy and maintain referential integrity.

---

# Database Summary

| Category     | Tables                                                          |
| ------------ | --------------------------------------------------------------- |
| Master Data  | Suppliers, SupplierContacts, Plants, ProductionLines, Employees |
| Product Data | PartCategories, Parts                                           |
| Procurement  | PurchaseOrders, PurchaseOrderLines                              |
| Operations   | Deliveries, Inspections                                         |
| Quality      | Defects, DefectCategories, RootCauses, CorrectiveActions        |
| Reporting    | SupplierAudits, Inventory, MonthlySupplierKPIs                  |

---

# Table Index

## Master Data

| No. | Table            |
| --: | ---------------- |
|   1 | Suppliers        |
|   2 | SupplierContacts |
|   3 | Plants           |
|   4 | ProductionLines  |
|   5 | Employees        |

## Product Data

| No. | Table          |
| --: | -------------- |
|   6 | PartCategories |
|   7 | Parts          |

## Procurement

| No. | Table              |
| --: | ------------------ |
|   8 | PurchaseOrders     |
|   9 | PurchaseOrderLines |

## Operations

| No. | Table       |
| --: | ----------- |
|  10 | Deliveries  |
|  11 | Inspections |

## Quality

| No. | Table             |
| --: | ----------------- |
|  12 | Defects           |
|  13 | DefectCategories  |
|  14 | RootCauses        |
|  15 | CorrectiveActions |

## Reporting

| No. | Table               |
| --: | ------------------- |
|  16 | SupplierAudits      |
|  17 | Inventory           |
|  18 | MonthlySupplierKPIs |

---

# Master Data

---

# Table 1 — Suppliers

### Business Purpose

Stores master information for all approved suppliers providing materials or components to the manufacturing organization.

### Primary Key

`SupplierID`

### Estimated Records

100

| Column             | Data Type    | Key | Description                                  |
| ------------------ | ------------ | --- | -------------------------------------------- |
| SupplierID         | VARCHAR(10)  | PK  | Unique supplier identifier                   |
| SupplierName       | VARCHAR(100) |     | Company name                                 |
| SupplierCategory   | VARCHAR(50)  |     | Electronics, Metal, Plastic, Fasteners, etc. |
| Country            | VARCHAR(50)  |     | Country                                      |
| State              | VARCHAR(50)  |     | State or Province                            |
| City               | VARCHAR(50)  |     | City                                         |
| ISO9001Certified   | BOOLEAN      |     | ISO 9001 certification                       |
| IATF16949Certified | BOOLEAN      |     | Automotive quality certification             |
| PreferredSupplier  | BOOLEAN      |     | Preferred supplier indicator                 |
| RiskLevel          | VARCHAR(20)  |     | Low, Medium, High                            |
| SupplierStatus     | VARCHAR(20)  |     | Active, Inactive                             |
| StartDate          | DATE         |     | Supplier onboarding date                     |

---

# Table 2 — SupplierContacts

### Business Purpose

Stores supplier contact information.

### Primary Key

`ContactID`

### Foreign Key

`SupplierID → Suppliers`

### Estimated Records

200

| Column      | Data Type    | Key | Description        |
| ----------- | ------------ | --- | ------------------ |
| ContactID   | VARCHAR(10)  | PK  | Contact identifier |
| SupplierID  | VARCHAR(10)  | FK  | Related supplier   |
| ContactName | VARCHAR(100) |     | Contact name       |
| JobTitle    | VARCHAR(100) |     | Position           |
| Email       | VARCHAR(100) |     | Email address      |
| Phone       | VARCHAR(25)  |     | Phone number       |

---

# Table 3 — Plants

### Business Purpose

Stores manufacturing plant information.

### Primary Key

`PlantID`

### Estimated Records

6

| Column      | Data Type    | Key | Description                             |
| ----------- | ------------ | --- | --------------------------------------- |
| PlantID     | VARCHAR(10)  | PK  | Plant identifier                        |
| PlantName   | VARCHAR(100) |     | Plant name                              |
| City        | VARCHAR(50)  |     | Plant city                              |
| State       | VARCHAR(50)  |     | State                                   |
| Country     | VARCHAR(50)  |     | Country                                 |
| PlantType   | VARCHAR(50)  |     | Assembly, Engine, Battery, Distribution |
| OpeningDate | DATE         |     | Plant opening date                      |

---

# Table 4 — ProductionLines

### Business Purpose

Stores production line information.

### Primary Key

`LineID`

### Foreign Key

`PlantID → Plants`

### Estimated Records

24

| Column         | Data Type   | Key | Description                |
| -------------- | ----------- | --- | -------------------------- |
| LineID         | VARCHAR(10) | PK  | Production line identifier |
| PlantID        | VARCHAR(10) | FK  | Parent plant               |
| LineName       | VARCHAR(50) |     | Production line name       |
| Shift          | VARCHAR(20) |     | Day, Evening, Night        |
| CapacityPerDay | INT         |     | Daily production capacity  |
| Status         | VARCHAR(20) |     | Active, Maintenance        |

---

# Table 5 — Employees

### Business Purpose

Stores employees participating in purchasing, production, quality, logistics, and supplier management.

### Primary Key

`EmployeeID`

### Foreign Key

`PlantID → Plants`

### Estimated Records

200

| Column           | Data Type    | Key | Description                     |
| ---------------- | ------------ | --- | ------------------------------- |
| EmployeeID       | VARCHAR(10)  | PK  | Employee identifier             |
| FirstName        | VARCHAR(50)  |     | First name                      |
| LastName         | VARCHAR(50)  |     | Last name                       |
| JobTitle         | VARCHAR(100) |     | Employee role                   |
| Department       | VARCHAR(50)  |     | Quality, Purchasing, Production |
| PlantID          | VARCHAR(10)  | FK  | Assigned plant                  |
| HireDate         | DATE         |     | Employment start date           |
| EmploymentStatus | VARCHAR(20)  |     | Active, Leave, Retired          |

---

# Product Data

---

# Table 6 — PartCategories

### Business Purpose

Stores standardized categories for manufactured parts.

### Primary Key

`PartCategoryID`

### Estimated Records

12

| Column         | Data Type   | Key | Description                                     |
| -------------- | ----------- | --- | ----------------------------------------------- |
| PartCategoryID | VARCHAR(10) | PK  | Category identifier                             |
| CategoryName   | VARCHAR(50) |     | Electrical, Engine, Interior, Exterior, Chassis |
| Description    | TEXT        |     | Category description                            |

---

# Table 7 — Parts

### Business Purpose

Stores part master data.

### Primary Key

`PartID`

### Foreign Keys

* `SupplierID → Suppliers`
* `PartCategoryID → PartCategories`

### Estimated Records

1,000

| Column         | Data Type     | Key | Description               |
| -------------- | ------------- | --- | ------------------------- |
| PartID         | VARCHAR(10)   | PK  | Part identifier           |
| SupplierID     | VARCHAR(10)   | FK  | Part supplier             |
| PartCategoryID | VARCHAR(10)   | FK  | Part category             |
| PartName       | VARCHAR(100)  |     | Part description          |
| Material       | VARCHAR(50)   |     | Material type             |
| UnitCost       | DECIMAL(10,2) |     | Cost per unit             |
| CriticalPart   | BOOLEAN       |     | Safety critical indicator |
| PartStatus     | VARCHAR(20)   |     | Active, Obsolete          |

---

# Procurement

---

# Table 8 — PurchaseOrders

### Business Purpose

Stores purchase order header information.

### Primary Key

`PO_ID`

### Foreign Keys

* `SupplierID → Suppliers`
* `PlantID → Plants`

### Estimated Records

20,000

| Column      | Data Type     | Key | Description               |
| ----------- | ------------- | --- | ------------------------- |
| PO_ID       | VARCHAR(15)   | PK  | Purchase order identifier |
| SupplierID  | VARCHAR(10)   | FK  | Supplier                  |
| PlantID     | VARCHAR(10)   | FK  | Receiving plant           |
| OrderDate   | DATE          |     | Order date                |
| DueDate     | DATE          |     | Expected delivery         |
| POStatus    | VARCHAR(20)   |     | Open, Closed, Delayed     |
| TotalAmount | DECIMAL(12,2) |     | Purchase order value      |

---

# Table 9 — PurchaseOrderLines

### Business Purpose

Stores line items belonging to purchase orders.

### Primary Key

`POLineID`

### Foreign Keys

* `PO_ID → PurchaseOrders`
* `PartID → Parts`

### Estimated Records

80,000

| Column          | Data Type     | Key | Description           |
| --------------- | ------------- | --- | --------------------- |
| POLineID        | VARCHAR(15)   | PK  | Purchase order line   |
| PO_ID           | VARCHAR(15)   | FK  | Parent purchase order |
| PartID          | VARCHAR(10)   | FK  | Ordered part          |
| OrderedQuantity | INT           |     | Quantity ordered      |
| UnitCost        | DECIMAL(10,2) |     | Unit cost             |
| LineTotal       | DECIMAL(12,2) |     | Extended cost         |

---

# Current Database Relationships

```text
Suppliers
│
├── SupplierContacts
├── Parts
├── PurchaseOrders
├── SupplierAudits
└── MonthlySupplierKPIs

Parts
│
└── PurchaseOrderLines

PurchaseOrders
│
└── PurchaseOrderLines

Plants
│
├── Employees
├── ProductionLines
├── PurchaseOrders
└── Inventory
```

---

# Current Record Summary

| Table              | Estimated Records |
| ------------------ | ----------------: |
| Suppliers          |               100 |
| SupplierContacts   |               200 |
| Plants             |                 6 |
| ProductionLines    |                24 |
| Employees          |               200 |
| PartCategories     |                12 |
| Parts              |             1,000 |
| PurchaseOrders     |            20,000 |
| PurchaseOrderLines |            80,000 |

**Current Estimated Records: ~101,542**

Operations
- Table 10 — Deliveries
- Table 11 — Inspections

Quality
- Table 12 — DefectCategories
- Table 13 — RootCauses
- Table 14 — Defects
- Table 15 — CorrectiveActions

Reporting
- Table 16 — SupplierAudits
- Table 17 — Inventory
- Table 18 — MonthlySupplierKPIs