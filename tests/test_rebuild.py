import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from rebuild_public_data import completed_years, rebuild


def employee(identifier="1", birth="1980-07-01", hire="2009-01-01", balance="15"):
    return [identifier, "fictional", "fictional", "", "", "Engineer", birth,
            "S", "F", hire, "1", "10", balance, "1", "guid", "2014-06-30"]


class RebuildTests(unittest.TestCase):
    def data(self):
        return {"Employee": [employee()], "Department": [["1", "Engineering"]],
                "EmployeeDepartmentHistory": [["1", "1", "1", "2009-01-01", "", "2014-06-30"]],
                "SalesPerson": [["1", "1", "", "0", "0", "125.5", "100"]],
                "SalesTerritory": [["1", "Northwest"]]}

    def test_age_uses_declared_date_not_modified_date(self):
        self.assertEqual(completed_years("1980-07-01", "2014-06-30"), 33)
        self.assertEqual(completed_years("1980-07-01", "2014-07-01"), 34)

    def test_balances_and_totals_reconcile(self):
        people, sales, summary = rebuild(self.data(), "2014-06-30")
        self.assertEqual(people[0]["AvailableSickLeaveHours"], 15)
        self.assertEqual(people[0]["SickLeaveBalanceBand"], "15 to 37.5 available hours")
        self.assertEqual(sum(summary["balance_bands"].values()), summary["current_employees"])
        self.assertEqual(summary["balance_bands"]["Below 15 available hours"], 0)
        self.assertEqual(sales[0]["SalesYTD"], "125.5")
        self.assertNotIn("absence_rate", summary)

    def test_duplicate_current_department_fails(self):
        data = self.data()
        data["EmployeeDepartmentHistory"] *= 2
        with self.assertRaisesRegex(ValueError, "current department"):
            rebuild(data, "2014-06-30")

    def test_future_dates_fail(self):
        with self.assertRaisesRegex(ValueError, "after"):
            completed_years("2020-01-01", "2014-06-30")

    def test_missing_department_is_not_silently_dropped(self):
        data = self.data()
        data["Department"] = []
        with self.assertRaisesRegex(ValueError, "department"):
            rebuild(data, "2014-06-30")

    def test_duplicate_sales_identity_fails(self):
        data = self.data()
        data["SalesPerson"] *= 2
        with self.assertRaisesRegex(ValueError, "SalesPerson"):
            rebuild(data, "2014-06-30")


if __name__ == "__main__":
    unittest.main()
