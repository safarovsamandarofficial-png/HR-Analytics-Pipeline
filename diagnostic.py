import pandas as pd

def run_diagnostic(df):
    """Prints a professional health report of the dataset."""
    print("=== DATA HEALTH REPORT ===")
    
    # 1. Structural Check
    print(f"\n[1] SHAPE: {df.shape[0]} rows | {df.shape[1]} columns")
    
    # 2. Missingness Audit (The "Holes")
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100
    missing_df = pd.DataFrame({'Missing': null_counts, 'Percentage': null_pct})
    print("\n[2] MISSING DATA MAP:")
    print(missing_df[missing_df['Missing'] > 0])
    
    # 3. Duplicate Check
    dupes = df.duplicated().sum()
    print(f"\n[3] DUPLICATES: {dupes} identical rows found.")
    
    # 4. Logical Consistency (Numeric Columns)
    print("\n[4] NUMERIC RANGE AUDIT:")
    stats = df.describe().loc[['min', 'max', 'mean']]
    print(stats)
    
    # 5. Cardinality (Category Check)
    print("\n[5] CATEGORICAL SKEW (Top 3 per column):")
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        top_vals = df[col].value_counts().head(3).to_dict()
        print(f" - {col}: {top_vals}")

    print("\n=== END OF REPORT ===")


def validate_df(df, label='DataFrame'):
    """
    Prints a quick health report for a DataFrame: missing values and duplicate rows.

    Args:
        df    : DataFrame to validate.
        label : A descriptive name shown in the report header.
    """
    print(f"\n{'='*50}")
    print(f"  Validation Report: {label}")
    print(f"{'='*50}")

    missing = df.isna().sum()
    missing_cols = missing[missing > 0]
    if missing_cols.empty:
        print("  ✅ Missing values : None")
    else:
        print("  ⚠️  Missing values:")
        for col, count in missing_cols.items():
            pct = count / len(df) * 100
            print(f"     {col}: {count} ({pct:.1f}%)")

    dupe_count = df.duplicated().sum()
    if dupe_count == 0:
        print("  ✅ Duplicate rows : None")
    else:
        print(f"  ⚠️  Duplicate rows : {dupe_count}")

    print(f"  📐 Shape          : {df.shape[0]} rows × {df.shape[1]} cols")
    print(f"{'='*50}\n")