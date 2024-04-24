import polars as pl

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
