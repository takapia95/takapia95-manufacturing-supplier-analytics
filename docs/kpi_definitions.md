# KPI Definitions

## Manufacturing Supplier Intelligence Platform

---

# Purpose

This document defines the key performance indicators used in the Manufacturing Supplier Intelligence Platform.

The KPIs measure supplier quality, delivery performance, inspection outcomes, corrective action effectiveness, cost impact, and overall supplier risk.

---

# KPI Categories

| Category               | Purpose                                     |
| ---------------------- | ------------------------------------------- |
| Supplier Quality       | Measures supplier defect performance        |
| Delivery Performance   | Measures supplier delivery reliability      |
| Inspection Performance | Measures incoming inspection results        |
| Corrective Action      | Measures issue resolution effectiveness     |
| Cost Performance       | Measures financial impact of quality issues |
| Risk Scoring           | Identifies high-risk suppliers              |

---

# Supplier Quality KPIs

## 1. Parts Per Million — PPM

### Purpose

Measures how many defective parts occur per one million received parts.

### Formula

```text
PPM = (Total Defective Quantity / Total Received Quantity) × 1,000,000
```

### Interpretation

| PPM Range | Performance       |
| --------: | ----------------- |
|     0–100 | Excellent         |
|   101–500 | Good              |
| 501–1,200 | Needs Improvement |
|    1,201+ | High Risk         |

---

## 2. Defect Rate

### Formula

```text
Defect Rate = (Defective Quantity / Inspected Quantity) × 100
```

### Interpretation

Lower defect rate indicates better incoming supplier quality.

---

## 3. Rejection Rate

### Formula

```text
Rejection Rate = (Rejected Quantity / Received Quantity) × 100
```

### Interpretation

Used to monitor how much received material fails quality acceptance.

---

## 4. Supplier Quality Score

### Formula

```text
Supplier Quality Score =
(Quality Performance × 0.40) +
(Delivery Performance × 0.25) +
(Audit Score × 0.20) +
(Corrective Action Performance × 0.15)
```

### Interpretation

|    Score | Rating            |
| -------: | ----------------- |
|   90–100 | Excellent         |
|    80–89 | Good              |
|    70–79 | Needs Improvement |
|    60–69 | High Risk         |
| Below 60 | Critical          |

---

# Delivery Performance KPIs

## 5. On-Time Delivery Rate

### Formula

```text
On-Time Delivery Rate = (On-Time Deliveries / Total Deliveries) × 100
```

### Interpretation

Measures supplier delivery reliability.

|  OTD Rate | Performance       |
| --------: | ----------------- |
|   95–100% | Excellent         |
|    90–94% | Good              |
|    80–89% | Needs Improvement |
| Below 80% | High Risk         |

---

## 6. Average Delay Days

### Formula

```text
Average Delay Days = Total Delay Days / Number of Late Deliveries
```

### Interpretation

Measures the average number of days late for delayed shipments.

---

## 7. Late Delivery Rate

### Formula

```text
Late Delivery Rate = (Late Deliveries / Total Deliveries) × 100
```

### Interpretation

Lower values indicate stronger supplier logistics performance.

---

# Inspection Performance KPIs

## 8. Average Inspection Score

### Formula

```text
Average Inspection Score = Sum of Inspection Scores / Number of Inspections
```

### Interpretation

Measures overall incoming inspection quality.

---

## 9. First Pass Yield

### Formula

```text
First Pass Yield = (Passed Quantity / Inspected Quantity) × 100
```

### Interpretation

Measures the percentage of parts that pass inspection without rework or rejection.

---

## 10. Inspection Failure Rate

### Formula

```text
Inspection Failure Rate = (Failed Inspections / Total Inspections) × 100
```

### Interpretation

Used to identify suppliers or plants with repeated inspection failures.

---

# Corrective Action KPIs

## 11. Open Corrective Actions

### Formula

```text
Open Corrective Actions = Count of CARs where Status is Open or In Progress
```

### Interpretation

Shows unresolved supplier quality issues.

---

## 12. CAR Closure Rate

### Formula

```text
CAR Closure Rate = (Closed CARs / Total CARs) × 100
```

### Interpretation

Measures how effectively quality issues are resolved.

---

## 13. Average CAR Closure Days

### Formula

```text
Average CAR Closure Days = Average(CloseDate - OpenDate)
```

### Interpretation

Measures how long it takes to close corrective actions.

---

## 14. Overdue CAR Rate

### Formula

```text
Overdue CAR Rate = (Overdue CARs / Total Open CARs) × 100
```

### Interpretation

High overdue rate indicates poor corrective action follow-up.

---

# Cost Performance KPIs

## 15. Scrap Cost

### Formula

```text
Scrap Cost = Scrap Quantity × Unit Cost
```

---

## 16. Rework Cost

### Formula

```text
Rework Cost = Rework Quantity × Estimated Rework Cost Per Unit
```

---

## 17. Cost of Poor Quality — COPQ

### Formula

```text
COPQ = Scrap Cost + Rework Cost + Inspection Cost + Corrective Action Cost
```

### Interpretation

Measures total financial impact of supplier quality problems.

---

## 18. Defect Cost

### Formula

```text
Defect Cost = Scrap Cost + Rework Cost
```

---

# Supplier Risk KPIs

## 19. Supplier Risk Score

### Formula

```text
Supplier Risk Score =
(PPM Risk × 0.35) +
(Delivery Risk × 0.25) +
(CAR Risk × 0.20) +
(Audit Risk × 0.20)
```

### Interpretation

| Risk Score | Risk Level |
| ---------: | ---------- |
|       0–25 | Low        |
|      26–50 | Medium     |
|      51–75 | High       |
|     76–100 | Critical   |

---

## 20. High-Risk Supplier Count

### Formula

```text
High-Risk Supplier Count = Count of suppliers where RiskLevel is High or Critical
```

---

# Plant Performance KPIs

## 21. Plant Rejection Rate

### Formula

```text
Plant Rejection Rate = (Total Rejected Quantity by Plant / Total Received Quantity by Plant) × 100
```

---

## 22. Plant Scrap Cost

### Formula

```text
Plant Scrap Cost = Sum of Scrap Cost by Plant
```

---

# Dashboard KPI Cards

The executive dashboard should include the following KPI cards:

* Total Suppliers
* High-Risk Suppliers
* Monthly PPM
* On-Time Delivery Rate
* Open Corrective Actions
* Scrap Cost
* Average Inspection Score
* Supplier Quality Score
* Total Defects
* Late Delivery Rate

---

# KPI Data Sources

| KPI                      | Main Source Tables                                     |
| ------------------------ | ------------------------------------------------------ |
| PPM                      | Deliveries, Inspections, Defects                       |
| Defect Rate              | Inspections, Defects                                   |
| Rejection Rate           | Deliveries                                             |
| Supplier Quality Score   | MonthlySupplierKPIs, SupplierAudits, CorrectiveActions |
| On-Time Delivery Rate    | Deliveries                                             |
| Average Delay Days       | Deliveries                                             |
| Average Inspection Score | Inspections                                            |
| First Pass Yield         | Inspections                                            |
| CAR Closure Rate         | CorrectiveActions                                      |
| Scrap Cost               | Defects, Parts                                         |
| COPQ                     | Defects, CorrectiveActions, Inspections                |
| Supplier Risk Score      | MonthlySupplierKPIs, SupplierAudits, CorrectiveActions |
| Plant Rejection Rate     | Plants, PurchaseOrders, Deliveries                     |

---

# Notes

* KPI formulas will be implemented in SQL views and Power BI DAX measures.
* Monthly KPI values will be stored in `MonthlySupplierKPIs` for faster dashboard performance.
* Operational KPIs will also be calculated directly from source tables for validation.
* Supplier scoring will use weighted formulas to simulate real-world scorecard logic.
