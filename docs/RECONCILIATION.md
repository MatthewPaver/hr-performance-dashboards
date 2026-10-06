# Reconciliation checklist

Run this checklist after rebuilding from AdventureWorks and before interpreting a visual.

1. Record the AdventureWorks backup filename/version, `REPORT_AS_OF_DATE`, extraction timestamp and row counts.
2. Assert one current department row per `BusinessEntityID`; investigate duplicates before aggregation.
3. Reconcile the three available-sick-leave bands to the current-employee total.
4. Assert `AgeYears >= 0`, `TenureYears >= 0`, `BirthDate <= REPORT_AS_OF_DATE` and `HireDate <= REPORT_AS_OF_DATE`.
5. Assert the top-performer table contains five rows, with the tie policy stated.
6. Reconcile `SalesYTD` and `SalesLastYear` totals before and after joining names/territories.
7. Confirm every visible label says *available sick-leave hours* rather than absence taken.
8. Treat the historical PBIX and PDF as delivery artefacts until their measures/labels are updated to this contract.

The package validator checks file presence and wording. `scripts/rebuild_public_data.py` downloads the commit-pinned public tables and runs data-level assertions in Python; `docs/rebuilt/summary.json` records source hashes and reconciled totals. These checks do not recalculate the historical Power BI model. Recheck its measures and visuals in Power BI after refreshing it from the corrected output.
