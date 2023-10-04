#### ATTEMPT 4.2.1 ####

import pandas as pd
import polars as pl
import numpy as np
from tqdm import tqdm

def combine_labels(df:pd.DataFrame, id_cols:list, label_cols:list, drop_duplicates:bool=True):
    """Combines the labels for each row of a DataFrame into a single label.

    Args:
        df: A Pandas DataFrame.
        id_cols: A list of column names that uniquely identify each row of the DataFrame.
        label_cols: A list of column names containing labels.

    Returns:
        A Pandas DataFrame with the combined labels.
    """

    df = df.reset_index(drop=True)

    # Create a NumPy array to store the combined labels.
    combined_labels = np.empty(len(df), dtype=object)

    # Group the DataFrame by the ID columns.
    grouped = df.groupby(id_cols)

    # Iterate over the groups.
    for ids, group in tqdm(grouped):
        # Create a list to store the labels for the current group.
        group_labels = []

        # Iterate over the label columns and add each label to the list.
        for label_col in label_cols:
            group_labels.extend(group[label_col].dropna())

        # Remove any empty strings or invalid labels from the list.
        #group_labels = [label for label in group_labels if label not in [' ', 999, 111]]

        # Convert float values to integers and remove any empty strings or invalid labels from the list.
        group_labels = set(int(label) if isinstance(label, float) else label for label in group_labels if label not in [' ', 999, 111])

        # Join the labels into a single string, separated by pipes (`|`).
        combined_labels[group.index] = '|'.join(map(str, group_labels))

    # Add the combined labels to the original DataFrame.
    df['Combined Labels'] = combined_labels

    if drop_duplicates:
      return df.drop_duplicates(subset=id_cols, keep='first', ignore_index=True)
    else:
      return df
                        
# Example usage:
# combined_df = combine_labels(your_dataframe, id_cols=['ID'], label_cols=['Label1', 'Label2'])


def combine_labels_polars(df:pl.DataFrame, id_cols:list, label_cols:list, label_considering:bool=True, to_str:bool=True):
    """Combines the labels for each row of a DataFrame into a single label.

    Args:
        df: A Polars DataFrame.
        id_cols: A list of column names that uniquely identify each row of the DataFrame.
        label_cols: A list of column names containing labels.

    Returns:
        A Polars DataFrame with the combined labels.
    """

    # Require Polars 0.19.5
    q_str = (
        df\
        .lazy()\
        .join(
            df\
            .lazy()\
            .group_by(by=id_cols)\
            .agg(
                pl.col(label_cols).filter(pl.col(label_cols).is_not_null()).cast(pl.Utf8),
            )\
            .with_columns(
                pl.concat_list(pl.col(label_cols)).map_elements(lambda x: list(set(x))).list.join('|').alias('Combined Labels'),
            )\
            .select(pl.col(id_cols + ['Combined Labels'])),
            on=id_cols,
        )\
        .unique(
            subset=id_cols,
            keep='any'
            )
    )

    q_list = (
        df\
        .lazy()\
        .join(
            df\
            .lazy()\
            .group_by(by=id_cols)\
            .agg(
                pl.col(label_cols).filter(pl.col(label_cols).is_not_null()).cast(pl.Utf8),
            )\
            .with_columns(
                pl.concat_list(pl.col(label_cols)).map_elements(lambda x: list(set(x))).alias('Combined Labels'),
            )\
            .select(pl.col(id_cols + ['Combined Labels'])),
            on=id_cols,
        )\
        .unique(
            subset=id_cols,
            keep='any'
            )
    )

    if label_considering:
        return q_str.collect() if to_str else q_list.collect()

    else:
        return df.unique(subset=id_cols, keep='any')

# Example usage:
# combined_df = combine_labels(your_dataframe, id_cols=['ID'], label_cols=['Label1', 'Label2'])

def one_hot_encode_polars(df: pl.DataFrame, id_cols: str|list[str], column: str, separator: str = '_', rename_encoded_cols: bool = False) -> pl.DataFrame:
    """Encodes the specified columns in the given dataframe.
    
    Args:
    df: The dataframe to encode.
    id_cols: The columns to use as the grouping columns.
    column: A column to encode.
    separator: The separator to use when creating the one-hot encoded columns.
    
    Returns:
    A dataframe with the encoded columns.
    """
    q = (
      df
      .explode(column)
      .to_dummies(columns=column, separator=separator)
      .group_by(id_cols)
      .agg(pl.all().max())
    )
    
    return rename_encoded_columns(q, column, separator) if rename_encoded_cols else q


def rename_encoded_columns(df: pl.DataFrame, column: str, separator: str = '_') -> pl.DataFrame:
    """Renames the encoded columns in the given dataframe.
    
    Args:
    df: The dataframe to rename the encoded columns in.
    column: The name of the column that the encoded columns start with.
    separator: The separator that is used between the column name and the encoded value.
    
    Returns:
    A dataframe with the renamed encoded columns.
    
    Raises:
    ValueError: If the `column` argument is not an encoded column.
    """
    assert isinstance(column, str)
    # Get the list of encoded columns.
    start_str = f'{column}{separator}'
    encoded_columns = df.select([column for column in df.columns if column.startswith(start_str)]).columns
    
    # Rename the encoded columns.
    for column in encoded_columns:
        df = df.rename({column: column.split(separator)[1]})
    
    return df
