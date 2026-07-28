import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SAMPLE = ROOT / "sample-data" / "hr-performance-synthetic.csv"


class SyntheticSampleTests(unittest.TestCase):
    def test_sample_has_expected_public_schema_and_50_rows(self):
        with SAMPLE.open(newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 50)
        self.assertEqual(
            set(rows[0]),
            {
                "employee_id",
                "department",
                "region",
                "age_band",
                "annual_sick_hours",
                "current_year_sales",
                "prior_year_sales",
                "performance_band",
            },
        )
        self.assertEqual(len({row["employee_id"] for row in rows}), 50)
        self.assertTrue(all(row["employee_id"].startswith("EMP-") for row in rows))
        self.assertGreaterEqual(len({row["department"] for row in rows}), 5)


if __name__ == "__main__":
    unittest.main()
