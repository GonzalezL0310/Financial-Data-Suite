"""
Data Storage Module (data_storage.py)

Responsible for saving DataFrames to disk.
"""

import pandas as pd

def save_data_to_csv(data: pd.DataFrame, ticker: str) -> None:
    """
    Saves the processed DataFrame to a CSV file.
    """
    if data is None or data.empty:
        print("Error: No data provided to save.")
        return

    filename = f"{ticker}_processed_data.csv"
    print(f"Saving data to '{filename}'...")

    try:
        data.to_csv(filename, index=True)
        print(f"Data successfully saved to '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving CSV: {e}")
