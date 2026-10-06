# Semantic contract and interpretation boundary

The bundled PBIX/PDF is a historical dashboard-delivery exercise. This contract is the current analytical interpretation and takes precedence over wording inside the historical export.

| Field | Defensible meaning | Do not claim |
| --- | --- | --- |
| `HumanResources.Employee.BirthDate` | Date of birth in the fictional sample | Age unless calculated against an explicit report as-of date |
| `HumanResources.Employee.HireDate` | Employment start date in the sample | Tenure unless calculated against an explicit report as-of date |
| `ModifiedDate` | The source row's last modification timestamp | Employee age, tenure, report date, employment duration or event date |
| `SickLeaveHours` | Available sick-leave hours stored on the employee record | Sick leave taken, an absence event, wellbeing, satisfaction, productivity or a cause of service performance |
| `VacationHours` | Available vacation hours stored on the employee record | Leave taken |
| `SalesYTD` | Sales attributed to the salesperson in the source's year-to-date period | A complete annual total unless the snapshot date is known |
| `SalesLastYear` | Prior-year comparison value supplied by AdventureWorks | Forecast growth, trend or causation |
| `TerritoryID` | AdventureWorks sales territory relationship | Employee location without verifying the model relationship |

## Required labels

- Use **available sick-leave hours**, not *absence*, *sick leave taken* or *days lost*.
- Use **descriptive comparison**, not *forecast*, *driver*, *root cause* or *correlation* unless a separately specified analysis supports it.
- Display `REPORT_AS_OF_DATE`, source release and refresh time beside age, tenure and YTD measures.
- Keep the middle sick-leave balance band visible so employee totals reconcile.
- “Top five” must contain exactly five rows after the report's declared tie policy.

## Decision boundary

This dataset can demonstrate relational modelling, DAX/SQL calculations, visual hierarchy and a stakeholder handoff. It cannot support action about a real employee and cannot establish that leave causes sales or service outcomes. Any reproduced report should be framed as a fictional BI exercise, not an HR diagnostic product.
