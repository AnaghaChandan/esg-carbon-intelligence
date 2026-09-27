import os

import pandas as pd


def load_activity_data(file_path):
    """
    Load ESG activity data from a CSV file.

    Parameters:
        file_path (str): Path to the activity data CSV file.

    Returns:
        pandas.DataFrame: Loaded activity data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Activity data file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("The activity data file is empty.")

    return df