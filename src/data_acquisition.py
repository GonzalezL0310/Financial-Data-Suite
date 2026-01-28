"""
Data Acquisition Module (data_acquisition.py)

Responsible for connecting to external sources (yfinance) 
and downloading raw data.
"""

import yfinance as yf
import pandas as pd
from typing import Optional

def download_historical_data(ticker: str, period: str) -> Optional[pd.DataFrame]:
    """
    Downloads historical OHLCV data for a given symbol and period.
    This function is 'pure': it does not depend on global configuration.
    """
    print(f"Starting data download for {ticker} (period: {period})...")
    try:
        asset = yf.Ticker(ticker)
        data: pd.DataFrame = asset.history(period=period)

        if data.empty:
            print(f"Error: No data found for {ticker} in period {period}.")
            return None

        print(f"Download complete. {len(data)} rows obtained.")

        standard_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        columns_to_keep = [col for col in standard_columns if col in data.columns]

        return data[columns_to_keep]

    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        return None

if __name__ == "__main__":
    print("--- Testing acquisition module in isolation ---")
    TEST_TICKER = "AAPL"
    TEST_PERIOD = "1y"
    test_data = download_historical_data(TEST_TICKER, TEST_PERIOD)
    if test_data is not None:
        print(f"Test successful for {TEST_TICKER}. First 3 rows:")
        print(test_data.head(3))
