# Reproduction guide

This is a historical Power BI exercise built from Microsoft's fictional AdventureWorks OLTP sample. It is reproducible as a method, but current AdventureWorks releases may contain adjusted dates and therefore will not necessarily produce the same ages, tenure, or year-to-date figures shown in the 2021 export.

## Fast data-only rebuild (no Power BI required)

Run `python3 scripts/rebuild_public_data.py --as-of 2014-06-30` from the repository root. This regenerates `docs/rebuilt/` from five official, commit-pinned Microsoft sample tables. `summary.json` records their hashes and rows, all three balance bands (including zero-count bands), and complete sales totals. Tests reject duplicate joins, missing departments and invalid reporting dates. The CSVs can also be imported into a new Power BI report.

This rebuild is not a refresh of the historical PBIX. Its age/tenure as-of date does not imply a common observation date for the separately supplied sales values. Sales totals remain descriptive and must not be turned into a year-on-year growth claim.

To regenerate the corrected one-page review, install the optional reporting dependency in a virtual environment and run:

```sh
python3 -m venv .venv-report
.venv-report/bin/pip install -r requirements-report.txt
.venv-report/bin/python scripts/render_review.py
```

The output is `output/pdf/corrected-hr-review.pdf`. This is a verified replacement summary, not a claim that the historical Power BI report has been refreshed.

## 1. Get the public source

Use Microsoft's official installation instructions and restore an AdventureWorks OLTP backup:

- [AdventureWorks installation guide](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure)
- [Microsoft SQL Server samples repository](https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works)

No employee information in this repository represents real people.

## 2. Rebuild the three analysis tables

The project documentation records the source relationships used for the report:

| Output | AdventureWorks inputs | Transformation |
| --- | --- | --- |
| Current employees | `HumanResources.vEmployeeDepartment`, `HumanResources.Employee` | Join on `BusinessEntityID`; select role, department, gender, birth date, hire date, and the person's name. Calculate age and tenure against a declared as-of date. |
| Sick-leave balance views | Current-employee output | Treat `SickLeaveHours` as **available sick-leave hours**, not leave taken. Keep below 15, 15–37.5 and above 37.5 bands visible so totals reconcile. |
| Sales performance | `Sales.SalesPerson`, `Sales.SalesTerritory`, `Person.Person` | Join on `BusinessEntityID` and `TerritoryID`; compare `SalesYTD` with `SalesLastYear` and retain territory/country context. |

For a faithful rerun, record the database release and choose an explicit as-of date. The original exercise used table modified dates for age/tenure; that is an invalid interpretation, not merely a stylistic preference. Use [`sql/adventureworks_review.sql`](../sql/adventureworks_review.sql) and the [`semantic contract`](SEMANTIC_CONTRACT.md) for the corrected calculations and labels.

## 3. Rebuild the report

Create three pages in Power BI:

1. Employee summary: department, age, gender, and tenure distributions with filters.
2. Available sick-leave balance review: threshold counts and departmental breakdowns. Do not describe this as absence taken.
3. Sales review: `SalesYTD` versus `SalesLastYear`, the top five representatives, and territory drill-down.

Open `HR Performance Reporting Dashboards.pbix` to inspect the historical data model, measures, filters, and visual interactions. Use the PDF export when Power BI Desktop is unavailable.

## 4. Validate the output

- Confirm employee totals reconcile across all available-leave balance bands, including zero-count bands.
- Confirm every sales representative maps to at most one person and territory.
- Treat `SalesYTD` versus `SalesLastYear` as descriptive unless the reporting period is known.
- Do not infer that absence causes performance changes from these dashboards.
- State the AdventureWorks release and as-of date alongside any reproduced figures.
- Complete the [`reconciliation checklist`](RECONCILIATION.md).

## What this demonstrates

The useful signal is the complete analytics handoff: relational source mapping, transformations, dashboard modelling, limitations, stakeholder explanation, and a static review route. It is not presented as an HR product or as causal analysis.
