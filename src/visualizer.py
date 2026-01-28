"""
Visualization Module (visualizer.py)

Responsible for creating and saving charts using Matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt

def plot_metrics(
    data: pd.DataFrame,
    ticker: str,
    price_col: str,
    short_sma_col: str,
    long_sma_col: str
) -> None:
    """
    Plots close price and Simple Moving Averages (SMA).
    """
    if data is None or data.empty:
        print("Error: No data provided for plotting.")
        return

    required_columns = [price_col, short_sma_col, long_sma_col]
    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        print(f"Plotting error: Missing columns: {missing_columns}")
        return

    filename = f"{ticker}_metrics_plot.png"

    try:
        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data[price_col], label='Close Price', color='blue', alpha=0.7)
        plt.plot(data.index, data[short_sma_col], label=short_sma_col, color='orange', linestyle='--')
        plt.plot(data.index, data[long_sma_col], label=long_sma_col, color='red', linestyle='--')

        plt.title(f'Close Price and Moving Averages for {ticker}', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        plt.close()
        print(f"Chart successfully saved as '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving the chart: {e}")
