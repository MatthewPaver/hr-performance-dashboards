"""Rebuild corrected, fictional AdventureWorks review tables without Power BI."""
import argparse
from collections import Counter
import csv
from datetime import date
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen

SOURCE_COMMIT = "fd84be9ed763069e4fdaf88f5983942c7d3a2821"
SOURCE = f"https://raw.githubusercontent.com/microsoft/sql-server-samples/{SOURCE_COMMIT}/samples/databases/adventure-works/oltp-install-script"
TABLES = ("Employee", "EmployeeDepartmentHistory", "Department", "SalesPerson", "SalesTerritory")


def completed_years(start, as_of):
    start, end = date.fromisoformat(start), date.fromisoformat(as_of)
    if start > end:
        raise ValueError("Birth/hire date is after the declared report date")
    return end.year - start.year - ((end.month, end.day) < (start.month, start.day))


def unique(rows, name):
    result = {row[0]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate identity in {name}")
    return result


def rebuild(tables, as_of):
    departments = unique(tables["Department"], "Department")
    current = unique([r for r in tables["EmployeeDepartmentHistory"] if not r[4]], "current department")
    employees = unique(tables["Employee"], "Employee")
    people = []
    for identifier, row in employees.items():
        if row[13] != "1":
            continue
        history = current.get(identifier)
        if history is None or history[1] not in departments:
            raise ValueError(f"Missing current department for employee {identifier}")
        balance = int(row[12])
        if balance < 0 or int(row[11]) < 0:
            raise ValueError("Negative available leave balance")
        band = "Below 15 available hours" if balance < 15 else (
            "Above 37.5 available hours" if balance > 37.5 else "15 to 37.5 available hours")
        people.append({"BusinessEntityID": identifier, "Department": departments[history[1]][1],
                       "AgeYears": completed_years(row[6], as_of),
                       "TenureYears": completed_years(row[9], as_of),
                       "AvailableSickLeaveHours": balance, "AvailableVacationHours": int(row[11]),
                       "SickLeaveBalanceBand": band, "ReportAsOfDate": as_of})
    territories = unique(tables["SalesTerritory"], "SalesTerritory")
    sales = []
    for identifier, row in unique(tables["SalesPerson"], "SalesPerson").items():
        if row[1] and row[1] not in territories:
            raise ValueError(f"Missing sales territory for salesperson {identifier}")
        sales.append({"BusinessEntityID": identifier,
                      "Territory": territories[row[1]][1] if row[1] else "Unassigned",
                      "SalesYTD": str(Decimal(row[5])), "SalesLastYear": str(Decimal(row[6]))})
    sales.sort(key=lambda r: (-Decimal(r["SalesYTD"]), int(r["BusinessEntityID"])))
    counts = Counter(p["SickLeaveBalanceBand"] for p in people)
    bands = {band: counts[band] for band in ("Below 15 available hours",
             "15 to 37.5 available hours", "Above 37.5 available hours")}
    return people, sales, {"report_as_of_date": as_of, "current_employees": len(people),
                           "balance_bands": bands, "salespeople": len(sales),
                           "sales_ytd_total": str(sum(Decimal(s["SalesYTD"]) for s in sales)),
                           "sales_last_year_total": str(sum(Decimal(s["SalesLastYear"]) for s in sales)),
                           "boundary": "Fictional sample balances, not absence taken. Sales snapshot periods are not established; no growth or causal claim."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", required=True, help="Explicit YYYY-MM-DD date for age/tenure only")
    parser.add_argument("--output", type=Path, default=Path("docs/rebuilt"))
    args = parser.parse_args()
    date.fromisoformat(args.as_of)
    tables, provenance = {}, {}
    for table in TABLES:
        url = f"{SOURCE}/{table}.csv"
        with urlopen(url, timeout=30) as response:
            raw = response.read(5_000_001)
        if len(raw) > 5_000_000:
            raise ValueError(f"Unexpected source size: {table}")
        tables[table] = list(csv.reader(io.StringIO(raw.decode("utf-8-sig")), delimiter="\t"))
        provenance[table] = {"url": url, "sha256": hashlib.sha256(raw).hexdigest(), "rows": len(tables[table])}
    people, sales, summary = rebuild(tables, args.as_of)
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, rows in (("current-employees.csv", people), ("sales.csv", sales), ("top-five-sales.csv", sales[:5])):
        with (args.output / filename).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    summary.update({"source_commit": SOURCE_COMMIT, "sources": provenance,
                    "licence": "Microsoft SQL Server samples MIT; see https://github.com/microsoft/sql-server-samples/blob/master/license.txt"})
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
