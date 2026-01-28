"""
Data Processing Module (data_processing.py)

Responsible for cleaning and transforming raw data, 
calculating technical metrics and features.
"""

import pandas as pd
import numpy as np
from typing import Optional

def process_financial_data(
    raw_data: pd.DataFrame,
    short_sma: int = 50,
    long_sma: int = 200,
    vol_period: int = 30
) -> Optional[pd.DataFrame]:
    """
    Processes raw OHLCV data to calculate technical metrics.
    """
    if raw_data is None or raw_data.empty:
        print("Error: No raw data provided for processing.")
        return None

    print(f"Starting data processing (SMA {short_sma}/{long_sma}, Vol {vol_period}d)...")
    df = raw_data.copy()

    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    df.index.name = 'Date'

    df['daily_returns'] = df['Close'].pct_change()

    short_sma_col = f'SMA_{short_sma}'
    long_sma_col = f'SMA_{long_sma}'
    df[short_sma_col] = df['Close'].rolling(window=short_sma).mean()
    df[long_sma_col] = df['Close'].rolling(window=long_sma).mean()

    volatility_col = f'Volatility_{vol_period}d'
    df[volatility_col] = df['daily_returns'].rolling(window=vol_period).std()

    print("Processing complete. Metrics calculated.")
    return df
