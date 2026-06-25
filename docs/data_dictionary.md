# Data Dictionary

## Manufacturing Supplier Intelligence Platform

---

# Overview

This document defines the database structure for the Manufacturing Supplier Intelligence Platform.

Each table includes:

* Purpose
* Primary Key
* Foreign Keys
* Column definitions
* Data types
* Business descriptions

The database follows Third Normal Form (3NF) to minimize redundancy and maintain referential integrity.

---

# Database Summary

| Category     | Tables                                                          |
| ------------ | --------------------------------------------------------------- |
| Master Data  | Suppliers, SupplierContacts, Plants, ProductionLines, Employees |
| Product Data | Parts, PartCategories                                           |
| Procurement  | PurchaseOrders, PurchaseOrderLines                              |
| Operations   | Deliveries, Inspections                                         |
| Quality      | Defects, DefectCategories, RootCauses, CorrectiveActions        |
| Reporting    | SupplierAudits, Inventory, MonthlySupplierKPIs                  |

---

# Table 1 — Suppliers

### Purpose

Stores supplier master information.

### Primary Key

SupplierID

### Estimated Records

100

| Column             | Data Type    | Key | Description                       |
| ------------------ | ------------ | --- | --------------------------------- |
| SupplierID         | VARCHAR(10)  | PK  | Unique supplier identifier        |
| SupplierName       | VARCHAR(100) |     | Company name                      |
| SupplierCategory   | VARCHAR(50)  |     | Electronics, Metal, Plastic, etc. |
| Country            | VARCHAR(50)  |     | Country                           |
| State              | VARCHAR(50)  |     | State or Province                 |
| City               | VARCHAR(50)  |     | City                              |
| ISO9001Certified   | BOOLEAN      |     | ISO 9001 certification            |
| IATF16949Certified | BOOLEAN      |     | Automotive quality certification  |
| PreferredSupplier  | BOOLEAN      |     | Preferred supplier flag           |
| RiskLevel          | VARCHAR(20)  |     | Low, Medium, High                 |
| SupplierStatus     | VARCHAR(20)  |     | Active, Inactive                  |
| StartDate          | DATE         |     | Supplier onboarding date          |

---

# Table 2 — SupplierContacts

### Purpose

Stores supplier contact information.

### Primary Key

ContactID

### Foreign Key

SupplierID → Suppliers

### Estimated Records

200

| Column      | Data Type    | Key | Description        |
| ----------- | ------------ | --- | ------------------ |
| ContactID   | VARCHAR(10)  | PK  | Contact identifier |
| SupplierID  | VARCHAR(10)  | FK  | Related supplier   |
| ContactName | VARCHAR(100) |     | Full name          |
| JobTitle    | VARCHAR(100) |     | Position           |
| Email       | VARCHAR(100) |     | Email address      |
| Phone       | VARCHAR(25)  |     | Phone number       |

---

# Table 3 — Plants

### Purpose

Stores manufacturing plant information.

### Primary Key

PlantID

### Estimated Records

6

| Column      | Data Type    | Key | Description                |
| ----------- | ------------ | --- | -------------------------- |
| PlantID     | VARCHAR(10)  | PK  | Plant identifier           |
| PlantName   | VARCHAR(100) |     | Plant name                 |
| City        | VARCHAR(50)  |     | Plant city                 |
| State       | VARCHAR(50)  |     | State                      |
| Country     | VARCHAR(50)  |     | Country                    |
| PlantType   | VARCHAR(50)  |     | Assembly, Engine, Stamping |
| OpeningDate | DATE         |     | Plant opening date         |

---

# Table 4 — ProductionLines

### Purpose

Stores production line information.

### Primary Key

LineID

### Foreign Key

PlantID → Plants

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

### Purpose

Stores employee information used throughout the system.

### Primary Key

EmployeeID

### Foreign Key

PlantID → Plants

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

# Current Relationships

```text
Suppliers
│
├── SupplierContacts
│
├── Parts
│
├── PurchaseOrders
│
├── SupplierAudits
│
└── CorrectiveActions


Plants
│
├── ProductionLines
│
├── Employees
│
├── PurchaseOrders
│
└── Inventory
```

---

# Master Data Summary

| Table            | Records |
| ---------------- | ------: |
| Suppliers        |     100 |
| SupplierContacts |     200 |
| Plants           |       6 |
| ProductionLines  |      24 |
| Employees        |     200 |

**Current total master records: ~530**
# Data Dictionary
