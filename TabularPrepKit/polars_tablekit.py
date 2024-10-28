import polars as pl
import numpy as np
from TabularPrepKit import helper_functions as helper

def drop_duplicates_multilabel(df: pl.DataFrame, id_cols: list, label_cols: list = None, label_considering: bool = True, to_str: bool = False, alias_str: str = 'decoded_label'):
    """Combines the labels for each row of a DataFrame into a single label.

    Args:
        df: A Polars DataFrame.
        id_cols: A list of column names that uniquely identify each row of the DataFrame.
        label_cols: A list of column names containing labels.

    Returns:
        A Polars DataFrame with the combined labels.
    """

    # Require Polars >=0.19.0
    q_str = (
        df\
        .lazy()\
        .join(
            df\
            .lazy()\
            .group_by(id_cols)\
            .agg(
                pl.col(label_cols).filter(pl.col(label_cols).is_not_null()).cast(pl.Utf8),
            )\
            .with_columns(
                pl.concat_list(pl.col(label_cols)).map_elements(lambda x: list(set(x))).list.join('|').alias(alias_str),
            )\
            .select(pl.col(id_cols + [alias_str])),
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
            .group_by(id_cols)\
            .agg(
                pl.col(label_cols).filter(pl.col(label_cols).is_not_null()).cast(pl.Utf8),
            )\
            .with_columns(
                pl.concat_list(pl.col(label_cols)).map_elements(lambda x: list(set(x))).alias(alias_str),
            )\
            .select(pl.col(id_cols + [alias_str])),
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
# combined_df = drop_duplicates_multilabel(your_dataframe, id_cols=['ID'], label_cols=['Label1', 'Label2'])

def one_hot_encoder(df: pl.DataFrame, id_cols: list[str], column: str = 'decoded_label', separator: str = '_', rename_encoded_cols: bool = False) -> pl.DataFrame:
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
    
    return helper.rename_encoded_columns(q, column, separator) if rename_encoded_cols else q

# Decoder procedures
def one_hot_decoder(df: pl.DataFrame, labels, sep='|', alias='decoded_label'):
  df = df.with_columns(
      [pl.when(pl.col(label).is_in([1])).then(pl.lit(label)).otherwise(pl.lit(None)).alias(label) for label in labels]
  ).with_columns(
      [pl.concat_list(labels).list.drop_nulls().list.join(sep).alias(alias)]
  )\
  .drop(labels)
  return df
