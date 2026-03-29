import pandas as pd

scores = {
    'Poor': 1,
    'Average': 2,
    'Good': 3,
    'Excellent': 4
}


def impute_employee_salaries(
    df,
    group_cols=['Department', 'Seniority_Level'],
    status_col='Status',
    salary_col='Salary',
    active_val='Active'
):
    """
    Fills missing salaries using a 3-layer hierarchical approach based on Active market rates.
    """
    df = df.copy()
    active_only = df[df[status_col] == active_val].copy()

    if active_only.empty:
        # FIX 1: Raise instead of silently continuing
        raise ValueError(
            f"Imputation failed: No rows found where '{status_col}' == '{active_val}'. "
            "Cannot derive market rates without Active employees."
        )

    # Layer 1: Group-level mean (Department + Seniority)
    df[salary_col] = df[salary_col].fillna(
        active_only.groupby(group_cols)[salary_col].transform('mean')
    )

    # Layer 2: Department-level mean
    dept_means = active_only.groupby(group_cols[0])[salary_col].mean()
    df[salary_col] = df[salary_col].fillna(df[group_cols[0]].map(dept_means))

    # Layer 3: Global mean
    global_mean = active_only[salary_col].mean()
    df[salary_col] = df[salary_col].fillna(global_mean)

    return df


def impute_age(df, age_col='Age', seniority_lvl='Seniority_Level'):
    """
    Fills missing ages using Seniority Level as the primary predictor.
    Logic: People with the same years of service are likely in a similar age bracket.
    """
    df = df.copy()

    # FIX 3: Use the parameter consistently instead of hardcoded string literals
    # Layer 1: Median age for that exact Seniority Level
    df[age_col] = df[age_col].fillna(
        df.groupby(seniority_lvl)[age_col].transform('median')
    )

    # Layer 2: Median age for the Department
    df[age_col] = df[age_col].fillna(
        df.groupby('Department')[age_col].transform('median')
    )

    # Layer 3: Global company median
    df[age_col] = df[age_col].fillna(df[age_col].median())

    # Final Touch: Round and convert to integer
    df[age_col] = df[age_col].round().astype(int)

    return df


def add_years_since(df, date_col, int_col_name='Years_Int', float_col_name='Years_Float'):
    """
    Computes years elapsed since a date column and adds two new columns to the DataFrame:
    one as a rounded integer and one as a float (1 decimal place).

    Args:
        df             : Input DataFrame.
        date_col       : Name of the date column to compute from.
        int_col_name   : Name for the new integer years column.
        float_col_name : Name for the new float years column.

    Returns:
        DataFrame with two new columns appended.
    """
    df = df.copy()
    parsed = pd.to_datetime(df[date_col], errors='coerce')
    time_passed = (pd.Timestamp.now() - parsed).dt.days / 365.25

    df[float_col_name] = time_passed.round(1)
    df[int_col_name] = time_passed.round().fillna(0).astype(int)

    return df


def ordinal_encoding(df, dictionary, column_name, numeric_col_name):
    """
    Maps a categorical column to ordinal integers using the provided dictionary.

    Raises:
        ValueError: If any unique values in the column are missing from the dictionary,
                    or if the count of unique values doesn't match the dictionary length.
    """
    df = df.copy()
    original_series = df[column_name].copy()

    processed_series = original_series.str.strip().str.title()
    unique_values = set(processed_series.dropna().unique())

    dict_keys = set(dictionary.keys())
    missing_from_dict = unique_values - dict_keys
    unused_in_dict = dict_keys - unique_values

    # FIX 1: Raise a detailed ValueError instead of printing and silently returning
    if missing_from_dict or len(unique_values) != len(dictionary):
        raise ValueError(
            f"Ordinal encoding failed for column '{column_name}'.\n"
            f"  Values in data not in dictionary : {missing_from_dict or 'None'}\n"
            f"  Keys in dictionary not in data   : {unused_in_dict or 'None'}\n"
            f"  Data unique values ({len(unique_values)}) : {sorted(unique_values)}\n"
            f"  Dictionary keys    ({len(dictionary)}) : {sorted(dict_keys)}"
        )

    df[numeric_col_name] = processed_series.map(dictionary)
    return df