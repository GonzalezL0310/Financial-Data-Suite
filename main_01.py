"""
Main Script (main.py)

Orchestrates the full data pipeline.
Injects configurations into logic modules.
"""

from data_acquisition import download_historical_data
from data_processing import process_financial_data
from data_storage import save_data_to_csv
from visualizer import plot_metrics
from config import (
    TICKER_SYMBOL,
    DATA_PERIOD,
    SHORT_SMA_PERIOD,
    LONG_SMA_PERIOD,
    VOLATILITY_PERIOD
)

def run_full_pipeline():
    """
    Main function to execute the data analysis pipeline.
    """
    print(f"=== Starting Analysis Pipeline for {TICKER_SYMBOL} ===")

    # STEP 1: DATA ACQUISITION
    raw_data = download_historical_data(TICKER_SYMBOL, DATA_PERIOD)
    if raw_data is None:
        return

    # STEP 2: PROCESSING
    processed_data = process_financial_data(
        raw_data,
        SHORT_SMA_PERIOD,
        LONG_SMA_PERIOD,
        VOLATILITY_PERIOD
    )
    if processed_data is None:
        return

    # STEP 3: STORAGE
    save_data_to_csv(processed_data, TICKER_SYMBOL)

    # STEP 4: VISUALIZATION
    short_sma_name = f'SMA_{SHORT_SMA_PERIOD}'
    long_sma_name = f'SMA_{LONG_SMA_PERIOD}'

    plot_metrics(
        processed_data,
        TICKER_SYMBOL,
        'Close',
        short_sma_name,
        long_sma_name
    )

    print(f"=== Pipeline completed successfully for {TICKER_SYMBOL} ===")

if __name__ == "__main__":
    run_full_pipeline()
