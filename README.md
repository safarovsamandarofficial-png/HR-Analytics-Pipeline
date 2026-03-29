
# 📊 HR Analytics Dashboard
**Executive Summary**: _An HR Analytics pipeline built by a Data analyst to identify payroll risks and workforce ROI._

---
## 📌 Overview

This project analyzes a **clean employee dataset** to generate **strategic business insights** for workforce planning, compensation fairness, and performance management. 

---
# 🚀 Features

- **Departmental Insights**: Attrition risk, salary distribution, performance alignment
- **Regional Insights**: Pay equity vs performance across states
- **Workforce Composition**: Remote vs in‑office, active vs inactive vs pending
- **Career Progression**: Tenure and seniority impact on performance
---
# 📈 Key Analyses

1. **Departmental Attrition Risk** → % inactive employees by department
2. **Regional Pay Equity** → Salary vs performance across regions
3. **Seniority ROI** → Performance vs salary by seniority level
4. **Pending Workforce Pipeline Health** → % pending employees by department/region
5. **Retention Risk Audit** → High performers underpaid relative to median
---

# 🎯 Recommendations

**Top 3 Issues**

- Fix underpayment of high performers
- Address attrition in Finance & Admin
- Streamline onboarding in Cloud Tech & Admin

**Top 2 Opportunities**

- Adjust pay equity in Nevada
- Invest in seniority level 5 employees (highest ROI group)

---
# 📂 Project Structure

# 📂 Project Structure

```text
├── analytics/              # Modular analytics functions
├── basic_cleaning.py       # Standard data cleaning logic
├── adv_cleaning.py         # Imputation & feature engineering
├── data_pipeline.py        # Executive script (Main Entry)
├── HR_Data_workbook.xlsx   # Final Dashboard & Visualization
├── Clean_Employee_dataset.csv 
└── README.md               # Documentation

---
# ⚙️ Tech Stack

- **Python** (Pandas, NumPy) for analysis.
- **Excel** for dashboard visualization.

---
# 📌 How to Use

1. Load the dataset (`Clean_Employee_dataset.csv`).
2. Run **data_pipeline.py** to generate full report.
3. Open Excel for visualization.
4. Review insights report for recommendations.
---

# Screenshots

Before:
![Before](/images/before.jpg)

After:
![After](/images/after.jpg)


Average Performance and Salary by Region chart:
![Chart_1](/images/chart1.png)


Departmental Attrition Risk chart:
![Chart_2](/images/chart2.png)


### Charts



# 🧠 Technical Challenges & Solutions

#### **1. Handling Deprecation & Future-Proofing**

During the development of the grouping logic, I encountered a `FutureWarning` regarding the `observed` parameter in the `groupby` function.

- **The Issue:** Pandas is shifting its default behavior for categorical groupings, which could lead to unexpected results (like empty categories appearing in the output) in future versions.
    
- **The Solution:** I explicitly implemented `observed=True` within the `pd.cut` aggregation. This ensures the analysis only returns categories present in the data, making the script more robust and silencing non-critical console noise.
#### **2. Logic over Loops**

Instead of using inefficient `for-loops` to categorize employee tenure, I implemented **vectorized binning** using `pd.cut()`. This approach allows the script to scale to datasets with hundreds of thousands of rows without a significant performance hit.

#### 3. Preserving Data Integrity (The Scientific Notation Trap)
During the diagnostic phase, I identified that phone numbers were being erroneously treated as float64 types, resulting in Scientific Notation (e.g., 4.94e+09) and loss of leading zeros.

The Issue: Pandas automatically infers long numeric strings as floats, which distorts categorical identifiers.

The Solution: I implemented a two-layer fix. First, I forced the dtype to str during the initial read_csv to prevent float conversion at the source. Second, I built a robust cleaning function using regex to strip artifacts like .0 and non-digit characters.

The Impact: This ensured 100% accuracy for employee contact data and removed non-analytical columns from numeric audits.
