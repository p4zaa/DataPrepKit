#### ATTEMPT 4.2.1 ####

import pandas as pd
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
        group_labels = [int(label) if isinstance(label, float) else label for label in group_labels if label not in [' ', 999, 111]]

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
