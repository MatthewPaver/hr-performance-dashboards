"""Render the corrected review PDF from the public-data rebuild. Requires reportlab."""
import csv
import json
from pathlib import Path
from collections import Counter
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

root = Path(__file__).resolve().parents[1]
summary = json.loads((root / "docs/rebuilt/summary.json").read_text())
with (root / "docs/rebuilt/current-employees.csv").open() as source:
    employees = list(csv.DictReader(source))
with (root / "docs/rebuilt/sales.csv").open() as source:
    sales = list(csv.DictReader(source))
assert len(employees) == summary["current_employees"] == sum(summary["balance_bands"].values())
assert sum(Decimal(r["SalesYTD"]) for r in sales) == Decimal(summary["sales_ytd_total"])
output = root / "output/pdf/corrected-hr-review.pdf"
output.parent.mkdir(parents=True, exist_ok=True)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="SmallNote", fontSize=9, leading=12, textColor=colors.HexColor("#43536A")))
styles["Title"].textColor = colors.HexColor("#1C3762")
story = []


def paragraph(text, style="BodyText"):
    story.append(Paragraph(text, styles[style]))
    story.append(Spacer(1, 8))


def table(rows, widths):
    item = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1C3762")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F0F4F8"), colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.extend([item, Spacer(1, 14)])


paragraph("HR data review: corrected interpretation", "Title")
paragraph("Matthew Paver | Fictional AdventureWorks sample | Rebuilt 5 September 2026", "SmallNote")
paragraph("This pack replaces the analytical interpretation, not the historical Power BI model. It demonstrates reproducible data preparation and reconciliation; it is not a tool for decisions about real employees.")
paragraph("Available leave is not absence", "Heading2")
table([["Available sick-leave balance", "Employees"],
       *[[band, str(count)] for band, count in summary["balance_bands"].items()],
       ["Total current employee records", str(len(employees))]], [380, 115])
paragraph("SickLeaveHours stores a remaining balance. None of these bands measures sick leave taken, productivity, wellbeing or absence risk. Zero-count and middle bands are retained so every employee reconciles.", "SmallNote")
paragraph("A reproducible employee snapshot", "Heading2")
department_counts = Counter(r["Department"] for r in employees)
largest = department_counts.most_common(1)[0]
paragraph(f"The rebuild retains {len(employees)} current employee records across {len(department_counts)} departments. {largest[0]} contains {largest[1]} records. Age and tenure use the declared calculation date {summary['report_as_of_date']}, never ModifiedDate. This calculation date is not a claim about the sales snapshot period.")
paragraph("Sales values: descriptive only", "Heading2")
table([["Supplied measure", "Total across 17 records"],
       ["SalesYTD", f"{Decimal(summary['sales_ytd_total']):,.4f}"],
       ["SalesLastYear", f"{Decimal(summary['sales_last_year_total']):,.4f}"]], [300, 195])
paragraph("The source does not establish comparable observation periods here, so no growth rate, forecast or causal conclusion is reported. The separate top-five CSV uses SalesYTD descending and employee ID ascending to break ties.", "SmallNote")
paragraph("Inspect and reproduce", "Heading2")
paragraph("Run <b>python3 scripts/rebuild_public_data.py --as-of 2014-06-30</b>. The docs/rebuilt directory contains employee and sales CSVs plus source URLs, row counts and SHA-256 hashes. Six regression tests check calculation dates, balance reconciliation and join failures.", "SmallNote")
paragraph(f"Source: Microsoft SQL Server samples, MIT. Commit {summary['source_commit'][:12]}. See docs/rebuilt/summary.json for immutable source links. Historical PBIX, PDFs, screenshots and video retain superseded labels until separately rebuilt in Power BI Desktop.", "SmallNote")
SimpleDocTemplate(str(output), pagesize=A4, rightMargin=50, leftMargin=50,
                  topMargin=36, bottomMargin=36, title="Corrected HR data review",
                  author="Matthew Paver").build(story)
print(output)
