# Synthetic HR performance sample

`hr-performance-synthetic.csv` contains 50 invented employee-level rows. It
shows the public field shape without redistributing the source records embedded
in the PBIX model. Employee IDs, departments, regions, ages, absence hours,
sales and performance bands are synthetic.

| Field | Meaning |
|:---|:---|
| `employee_id` | Synthetic stable identifier |
| `department` | Example organisational function |
| `region` | Example reporting region |
| `age_band` | Coarse age range rather than a birth date |
| `annual_sick_hours` | Illustrative annual absence hours |
| `current_year_sales` | Illustrative current-period sales amount |
| `prior_year_sales` | Illustrative comparison-period sales amount |
| `performance_band` | Illustrative review category |

The sample is suitable for schema inspection and test exercises. It does not
reproduce the dashboard's published measures or support conclusions about any
real employee or organisation.
