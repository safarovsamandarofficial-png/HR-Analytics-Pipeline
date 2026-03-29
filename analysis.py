import pandas as pd

def generate_business_insights(df):
    print("\n" + "="*50)
    print("      STRATEGIC BUSINESS INSIGHTS")
    print("="*50)
    
    # 1. Labor Cost Concentration
    dept_spend = df.groupby('Department')['Salary'].sum().sort_values(ascending=False)
    top_dept = dept_spend.index[0]
    print(f"💰 HIGHEST COST CENTER: {top_dept} (${dept_spend.max():,.2f})")
    
    # 2. Performance-to-Pay Alignment (The ACCA Logic)
    # Check if we are overpaying low performers or underpaying stars
    avg_pay_perf = df.groupby('Performance_Score_Numeric')['Salary'].mean()
    print("\n📊 AVERAGE SALARY BY PERFORMANCE:")
    print(avg_pay_perf)
    
    # 3. Retention Risk Audit
    # High-performing 'Seniors' with low relative pay
    median_salary = df['Salary'].median()
    at_risk = df[(df['Performance_Score_Numeric'] >= 3) & (df['Salary'] < median_salary)]
    print(f"\n⚠️ RETENTION RISK: {len(at_risk)} high-performers are paid below the company median.")
    
    print("="*50)


def remote_office_comparison_ps(df):

    response = df.groupby('Remote_Work')['Performance_Score_Numeric'].mean()

    inoffice_val = response[False]
    remote_val = response[True]

    print('Average Performance Scores of In Office vs Remote employees:')
    print(f'In Office: {inoffice_val:.2f}')
    print(f'Remote: {remote_val:.2f}')

    return response



def onboarding_effectiveness(df):
    """
    Measure performance distribution among employees with <2 years of service.
    High ROI: reveals if new hires are being integrated successfully.
    """
    bins = [0, 2, float('inf')]
    labels = ['New Hires', 'Tenured']

    grouped = df.groupby(pd.cut(df['Years_Serviced'], bins=bins, labels=labels), observed=True)['Performance_Score_Numeric'].mean()
    grouped = grouped.reset_index()
    print(grouped)

    return grouped


def departmental_attrition_risk(df):
    """
    Calculate inactive % by department.
    High ROI: pinpoints departments with highest turnover risk.
    """

    dept_counts = df.groupby("Department")["Status"].count()
    inactive_counts = df[df["Status"] == "Inactive"].groupby("Department")["Status"].count()
    risk = (inactive_counts / dept_counts * 100).fillna(0).reset_index()
    risk.columns = ["Department", "Inactive_Percentage"]
    risk['Inactive_Percentage'] = risk['Inactive_Percentage'].round(2)

    risk = risk.sort_values("Inactive_Percentage", ascending=False)
    print(risk)
    return risk


def regional_pay_equity(df):
    """
    Compare average salary vs average performance score across regions.
    """
    equity = df.groupby("Region").agg(
        Avg_Salary=("Salary", "mean"),
        Avg_Performance=("Performance_Score_Numeric", "mean")
    ).reset_index()

    equity['Avg_Salary'] = equity['Avg_Salary'].round().astype(int)
    equity['Avg_Performance'] = equity['Avg_Performance'].round(2)
    equity = equity.sort_values("Avg_Salary", ascending=False)
    print(equity)
    return equity


def seniority_performance_roi(df):
    """
    Compare performance scores across seniority levels.
    """
    roi = df.groupby("Seniority_Level").agg(
        Avg_Performance=("Performance_Score_Numeric", "mean"),
        Avg_Salary=("Salary", "mean"),
        Employee_Count=("Employee_Id", "count")
    ).reset_index()

    roi['Avg_Performance'] = roi['Avg_Performance'].round(2)
    roi['Avg_Salary'] = roi['Avg_Salary'].round().astype(int)

    roi = roi.sort_values("Seniority_Level")
    print(roi)
    return roi

def pending_pipeline_health(df):
    """
    Track % of Pending employees by department and region.
    """
    pending_counts = df[df["Status"] == "Pending"].groupby(["Department", "Region"])["Status"].count()
    total_counts = df.groupby(["Department", "Region"])["Status"].count()
    pipeline = (pending_counts / total_counts * 100).fillna(0).reset_index()
    pipeline.columns = ["Department", "Region", "Pending_Percentage"]
    pipeline['Pending_Percentage'] = pipeline['Pending_Percentage'].round(2)

    pipeline = pipeline.sort_values("Pending_Percentage", ascending=False)
    print(pipeline)
    return pipeline


def executive_summary():
    print("""
    KEY TAKEAWAYS:
    - DevOps is the highest cost center ($16.26M total salary)
    - 265 high-performing employees are underpaid relative to company median
    - Finance shows the highest attrition risk (36.47% inactive)
    - Regional pay-performance imbalance detected (Nevada has highest performance but lowest pay)
    - Pending workforce pipeline bottlenecks in Cloud Tech (Texas) and Admin (New York)
    """)


