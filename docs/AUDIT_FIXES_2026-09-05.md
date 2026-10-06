# Audit fixes — 5 September 2026

## Verified locally

- Rebuilt five official, commit-pinned AdventureWorks sample tables without Power BI or a private database. Source hashes and URLs accompany the output.
- Corrected leave interpretation: available balances, not annual absence. All three bands reconcile to 290 fictional employees, including the zero-count band.
- Age and tenure use birth/hire dates and an explicit 2014-06-30 as-of date, not row modification dates.
- Sales joins reject duplicate identities and missing referenced territories. All 17 representatives and the top five are exported separately; totals are descriptive, not a growth estimate.
- Six transformation tests pass, including negative join/date cases. The public download and CSV rebuild completed.
- A corrected one-page PDF was generated from the rebuilt files, rendered and visually checked. CI now tests transformations and checks deterministic output against the pinned source.

## Not completed or implied

The original PBIX, original PDF and historical screenshots have **not** been recalculated. Refreshing the Power BI model requires Power BI Desktop and manual visual/model verification. They remain explicitly historical; the new CSVs and corrected PDF are the current verified data handoff. No changes in this pass have been committed or published.
