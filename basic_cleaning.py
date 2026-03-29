import re
import pandas as pd

def split_and_expand(df, target_col, separator='-', new_headers=None):
    df = df.copy()
    split_data = df[target_col].str.split(separator, expand=True)

    if new_headers:
        split_data.columns = new_headers

    for col in split_data.columns:
        split_data[col] = split_data[col].str.strip().str.title()

    df = pd.concat([df, split_data], axis=1)
    df = df.drop(columns=[target_col])

    return df


def clean_phone_numbers(col):
    # 1. Convert to numeric first to handle any existing scientific notation
    # 2. Convert to 'Int64' to prevent the '.0' decimal issue
    # 3. Finally, convert to string for regex cleaning
    col_numeric = pd.to_numeric(col, errors='coerce')
    col_str = col_numeric.fillna(0).astype('Int64').astype(str)

    # Remove the '0' we used for fillna and clean any non-digits
    col_str = col_str.replace('0', '').str.replace(r'[^\d]+', '', regex=True)
    
    return col_str



def clean_columns(df):
    df = df.copy()
    df = df.rename(columns=lambda x: x.strip().title().replace(' ', '_').replace('-', '_'))
    return df


def check_drop_duplicates(df, subset=None):
    df = df.copy()
    if subset is None:
        subset = df.columns.tolist()
    if df.duplicated(subset=subset).sum() > 0:
        print('⚠️ DataFrame contained duplicates — dropping them.')
        df = df.drop_duplicates(subset=subset)
        return df
    
    print('No duplicates were found.')
    return df