import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file));
const text = (file) => read(file).toString("utf8");

const files = [
  "HR Performance Reporting Dashboards.pbix",
  "HR Performance Reporting Dashboards.pdf",
  "Project A HR Performance Reporting Documentation.pdf",
  "Dashboard Images/HR Performance Reporting Sales.png",
  "Dashboard Images/HR Performance Reporting Sick Leave.png",
  "Dashboard Images/HR Performance Reporting Summary.png",
  "README.md",
  "docs/reproduce.md",
  "docs/SEMANTIC_CONTRACT.md",
  "docs/RECONCILIATION.md",
  "sql/adventureworks_review.sql",
  "docs/rebuilt/summary.json",
  "docs/rebuilt/current-employees.csv",
  "docs/rebuilt/sales.csv",
  "output/pdf/corrected-hr-review.pdf",
];

for (const file of files) {
  assert.ok(fs.existsSync(path.join(root, file)), `Missing handoff file: ${file}`);
  assert.ok(fs.statSync(path.join(root, file)).size > 0, `Empty handoff file: ${file}`);
}

assert.equal(read("HR Performance Reporting Dashboards.pbix").subarray(0, 2).toString(), "PK", "PBIX package is not a valid archive");
for (const file of files.filter((name) => name.endsWith(".pdf"))) {
  assert.equal(read(file).subarray(0, 4).toString(), "%PDF", `Invalid PDF header: ${file}`);
}
for (const file of files.filter((name) => name.endsWith(".png"))) {
  assert.equal(read(file).subarray(1, 4).toString(), "PNG", `Invalid PNG header: ${file}`);
}

const readme = text("README.md");
const reproduce = text("docs/reproduce.md");
const semantics = text("docs/SEMANTIC_CONTRACT.md");
const sql = text("sql/adventureworks_review.sql");
assert.match(readme, /AdventureWorks/i, "README must name the sample data source");
assert.match(readme, /docs\/reproduce\.md/, "README must link to the reproduction guide");
assert.match(reproduce, /learn\.microsoft\.com\/en-us\/sql\/samples\/adventureworks-install-configure/, "Reproduction guide must link to Microsoft's source instructions");
assert.match(reproduce, /limitation/i, "Reproduction guide must state its limits");
assert.match(semantics, /available sick-leave hours/i, "Semantic contract must define SickLeaveHours correctly");
assert.match(semantics, /ModifiedDate[\s\S]{0,160}Employee age, tenure/i, "Semantic contract must reject ModifiedDate-derived age/tenure");
assert.match(sql, /@REPORT_AS_OF_DATE/, "Corrected SQL must use an explicit report date");
assert.doesNotMatch(sql, /DATEDIFF\([^\n]*ModifiedDate/i, "Corrected SQL must not derive age/tenure from ModifiedDate");
assert.doesNotMatch(readme, /identify root causes and take action/i, "README must not retain causal HR claims");

console.log(`Validated ${files.length} HR analytics handoff files.`);
