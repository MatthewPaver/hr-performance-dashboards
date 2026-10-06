/*
  Corrected, reproducible source queries for the AdventureWorks dashboard.
  Change this date deliberately and display it in the report. Never substitute
  ModifiedDate for the reporting date.
*/
DECLARE @REPORT_AS_OF_DATE date = '2025-12-31';

WITH CurrentEmployees AS (
  SELECT
    e.BusinessEntityID,
    p.FirstName,
    p.LastName,
    d.Name AS Department,
    e.JobTitle,
    e.Gender,
    e.BirthDate,
    e.HireDate,
    e.SickLeaveHours AS AvailableSickLeaveHours,
    e.VacationHours AS AvailableVacationHours,
    DATEDIFF(year, e.BirthDate, @REPORT_AS_OF_DATE)
      - CASE WHEN DATEADD(year, DATEDIFF(year, e.BirthDate, @REPORT_AS_OF_DATE), e.BirthDate) > @REPORT_AS_OF_DATE THEN 1 ELSE 0 END AS AgeYears,
    DATEDIFF(year, e.HireDate, @REPORT_AS_OF_DATE)
      - CASE WHEN DATEADD(year, DATEDIFF(year, e.HireDate, @REPORT_AS_OF_DATE), e.HireDate) > @REPORT_AS_OF_DATE THEN 1 ELSE 0 END AS TenureYears,
    @REPORT_AS_OF_DATE AS ReportAsOfDate
  FROM HumanResources.Employee AS e
  JOIN Person.Person AS p ON p.BusinessEntityID = e.BusinessEntityID
  JOIN HumanResources.EmployeeDepartmentHistory AS edh
    ON edh.BusinessEntityID = e.BusinessEntityID AND edh.EndDate IS NULL
  JOIN HumanResources.Department AS d ON d.DepartmentID = edh.DepartmentID
  WHERE e.CurrentFlag = 1
)
SELECT
  *,
  CASE
    WHEN AvailableSickLeaveHours < 15 THEN 'Below 15 available hours'
    WHEN AvailableSickLeaveHours > 37.5 THEN 'Above 37.5 available hours'
    ELSE '15 to 37.5 available hours'
  END AS SickLeaveBalanceBand
FROM CurrentEmployees;

-- Descriptive sales comparison. Do not label the difference as forecast growth
-- unless the source snapshot date and comparable periods are established.
SELECT TOP (5)
  sp.BusinessEntityID,
  p.FirstName,
  p.LastName,
  st.Name AS Territory,
  sp.SalesYTD,
  sp.SalesLastYear,
  sp.SalesYTD - sp.SalesLastYear AS DescriptiveDifference,
  @REPORT_AS_OF_DATE AS ReportAsOfDate
FROM Sales.SalesPerson AS sp
JOIN Person.Person AS p ON p.BusinessEntityID = sp.BusinessEntityID
LEFT JOIN Sales.SalesTerritory AS st ON st.TerritoryID = sp.TerritoryID
ORDER BY sp.SalesYTD DESC, sp.BusinessEntityID ASC;
