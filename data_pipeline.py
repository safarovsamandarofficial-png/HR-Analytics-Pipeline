import pandas as pd
import numpy as np
from thefuzz import process, fuzz
from diagnostic import run_diagnostic, validate_df

from basic_cleaning import *
from adv_cleaning import *
from analysis import *


df = pd.read_csv('data/raw/Messy_Employee_dataset.csv', dtype={'Phone': str})


def cleaning_ordered(df):
    
    df = check_drop_duplicates(df)
    df = clean_columns(df)

    df['Phone'] = clean_phone_numbers(df['Phone'])
    print(df['Phone'].dtype)
    df = add_years_since(df, 'Join_Date', 'Seniority_Level', 'Years_Serviced')
    df = split_and_expand(df, 'Department_Region', new_headers=['Department', 'Region'])
    
    df = ordinal_encoding(df, scores, 'Performance_Score', 'Performance_Score_Numeric')
    
    df = impute_employee_salaries(df, ['Department', 'Seniority_Level'], 'Status', 'Salary', active_val='Active')
    df = impute_age(df, 'Age', 'Seniority_Level')
    
    
    validate_df(df)
    df.to_csv('data/processed/Clean_Employee_dataset.csv', index=False)


def generate_full_report(df):
    print("\n" + "="*60)
    print("        MASTER HR ANALYTICS REPORT")
    print("="*60)

    # Executive Summary
    executive_summary()

    # Strategic Business Insights
    generate_business_insights(df)

    # Remote vs Office Comparison
    remote_office_comparison_ps(df)

    # Onboarding Effectiveness
    print("\nOnboarding Effectiveness (Performance of New Hires vs Tenured):")
    onboarding_effectiveness(df)

    # Departmental Attrition Risk
    print("\nDepartmental Attrition Risk (% Inactive Employees):")
    departmental_attrition_risk(df)

    # Regional Pay Equity
    print("\nRegional Pay Equity (Salary vs Performance):")
    regional_pay_equity(df)

    # Seniority ROI
    print("\nSeniority ROI (Performance vs Salary by Seniority Level):")
    seniority_performance_roi(df)

    # Pending Workforce Pipeline Health
    print("\nPending Workforce Pipeline Health (% Pending Employees):")
    pending_pipeline_health(df)

    print("="*60)
    print("        END OF REPORT")
    print("="*60)

def main(df):

    run_diagnostic(df)

    generate_full_report(df) # Generates analytics report


if __name__ == "__main__":
    main(df)