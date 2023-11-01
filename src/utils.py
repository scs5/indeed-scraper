import pandas as pd
import Levenshtein as lev

def remove_duplicates(data_fn, threshold=15):
    """Removes duplicate rows from a DataFrame based on similarity of descriptions and titles.

    Args:
        data_fn (str): The file name of the CSV containing the data.
        threshold (int, optional): The maximum Levenshtein distance to consider as a duplicate (default is 15).

    Returns:
        pd.DataFrame: A DataFrame with duplicate rows removed.
    """

    # Load data
    data = pd.read_csv(data_fn)

    # Create a set to store indices of rows to be removed
    rows_to_remove = set()

    # Iterate through the data
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            # Calculate the Levenshtein distance between descriptions
            distance = lev.distance(data.iloc[i]['Description'], data.iloc[j]['Description'])
            
            # If the distance is below the threshold and titles match, mark the row for removal
            if (distance <= threshold) and (data.iloc[i]['Title'] == data.iloc[j]['Title']):
                rows_to_remove.add(j)

    print('Number of duplicate rows removed:', len(rows_to_remove))

    # Remove duplicate rows
    rows_to_remove = list(rows_to_remove)
    data = data.drop(index=rows_to_remove).reset_index(drop=True)

    return data