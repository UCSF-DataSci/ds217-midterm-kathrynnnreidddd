# TODO: Add shebang line: #!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.
#
# These utilities will be imported and used in Q4-Q7 notebooks.

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.

    Args:
        filepath: Path to CSV file

    Returns:
        pd.DataFrame: Loaded data

    Example:
        >>> df = load_data('data/clinical_trial_raw.csv')
        >>> df.shape
        (10000, 18)
    """
    return pd.read_csv(filepath)
    pass


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates and replace sentinel values with NaN.

    Args:
        df: Input DataFrame
        remove_duplicates: Whether to drop duplicate rows
        sentinel_value: Value to replace with NaN (e.g., -999, -1)

    Returns:
        pd.DataFrame: Cleaned data

    Example:
        >>> df_clean = clean_data(df, sentinel_value=-999)
    """
    if remove_duplicates:
        df = df.drop_duplicates()
    df = df.replace(sentinel_value, np.nan)
    return df
    pass


def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Return count of missing values per column.

    Args:
        df: Input DataFrame

    Returns:
        pd.Series: Count of missing values for each column

    Example:
        >>> missing = detect_missing(df)
        >>> missing['age']
        15
    """
    return df.isnull().sum()
    pass


def fill_missing(df, column, strategy):
    out = df.copy()
    """
    Fill missing values in a column using specified strategy.

    Args:
        df: Input DataFrame
        column: Column name to fill
        strategy: Fill strategy - 'mean', 'median', or 'ffill'

    Returns:
        pd.DataFrame: DataFrame with filled values

    Example:
        >>> df_filled = fill_missing(df, 'age', strategy='median')
    """
    if strategy in ("mean", "median"):
        val = getattr(out[column].astype(float), strategy)()
        out[column] = out[column].fillna(val)
    elif strategy == "ffill":
        out[column] = out[column].ffill()
    else:
        raise ValueError("Unknown strategy")
    return out
    pass


def filter_data(df, filters):
    """
    Apply multiple filtering conditions to a DataFrame.
    """
    out = df.copy()
    for f in filters:
        col = f["column"]
        cond = f.get("condition", f.get("operator"))
        val = f["value"]

        if cond == "equals":
            out = out[out[col] == val]
        elif cond == "greater_than":
            out = out[out[col] > val]
        elif cond == "less_than":
            out = out[out[col] < val]
        elif cond == "in_range":
            lo, hi = val
            out = out[(out[col] >= lo) & (out[col] <= hi)]
        elif cond == "in_list":
            out = out[out[col].isin(val)]
        else:
            raise ValueError(f"Unknown condition: {cond}")
    return out
    pass


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    """
    Convert column data types based on mapping.

    Args:
        df: Input DataFrame
        type_map: Dict mapping column names to target types
                  Supported types: 'datetime', 'numeric', 'category', 'string'

    Returns:
        pd.DataFrame: DataFrame with converted types

    Example:
        >>> type_map = {
        ...     'enrollment_date': 'datetime',
        ...     'age': 'numeric',
        ...     'site': 'category'
        ... }
        >>> df_typed = transform_types(df, type_map)
    """
    for col, t in type_map.items():
        if t == 'datetime':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif t == 'numeric':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif t == 'category':
            df[col] = df[col].astype('category')
    return df
    pass

def create_bins(df: pd.DataFrame, column: str, bins: list, labels: list, new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().

    Args:
        df: Input DataFrame
        column: Column to bin
        bins: List of bin edges
        labels: List of bin labels
        new_column: Optional name for new binned column (default: '{column}_bins')

    Returns:
        pd.DataFrame: DataFrame with new binned column
    """
    out = df.copy()
    colname = new_column or f"{column}_bins"
    out[colname] = pd.cut(out[column], bins=bins, labels=labels, include_lowest=True)
    return out


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    """
    Group data and apply aggregations.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: aggregation_function(s)}
                  If None, uses .describe() on numeric columns

    Returns:
        pd.DataFrame: Grouped and aggregated data

    Examples:
        >>> # Simple summary
        >>> summary = summarize_by_group(df, 'site')
        >>>
        >>> # Custom aggregations
        >>> summary = summarize_by_group(
        ...     df,
        ...     'site',
        ...     {'age': ['mean', 'std'], 'bmi': 'mean'}
        ... )
    """
    if agg_dict is None:
        agg_dict = {col: 'mean' for col in df.select_dtypes(include=[np.number]).columns}
    return df.groupby(group_col).agg(agg_dict).reset_index()
    pass




if __name__ == '__main__':
    print("Data utilities loaded successfully!")
    print("Available functions:")
    print("  - load_data()")
    print("  - clean_data()")
    print("  - detect_missing()")
    print("  - fill_missing()")
    print("  - filter_data()")
    print("  - transform_types()")
    print("  - create_bins()")
    print("  - summarize_by_group()")
    
    # TODO: Add simple test example here
    # Example:
    # test_df = pd.DataFrame({'age': [25, 30, 35], 'bmi': [22, 25, 28]})
    # print("Test DataFrame created:", test_df.shape)
    # print("Test detect_missing:", detect_missing(test_df))