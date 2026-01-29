import os
import pandas as pd
import matplotlib.pyplot as plt
from .config_loader import settings

def plot_metrics(
    data: pd.DataFrame,
    ticker: str,
    price_col: str,
    short_sma_col: str,
    long_sma_col: str
) -> None:
    """
    Plots close price and Simple Moving Averages (SMA).
    Saves the output in a dedicated 'metrics' folder.
    """
    output_dir = settings['visualizer']['output_dir']
    f_size = tuple(settings['visualizer']['figure_size'])
    alpha_val = settings['visualizer']['line_alpha']

    if data is None or data.empty:
        print(f"Error: No data provided for {ticker}.")
        return

    # Encapsulated folder logic: keeps the function signature intact
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, f"{ticker}_metrics_plot.png")

    try:
        plt.figure(figsize=f_size)
        plt.plot(data.index, data[price_col], label='Close Price', alpha=alpha_val)
        plt.plot(data.index, data[short_sma_col], label=f'SMA {short_sma_col}')
        plt.plot(data.index, data[long_sma_col], label=f'SMA {long_sma_col}')

        plt.title(f"Market Analysis: {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        
        plt.savefig(filename)
        plt.close()
        print(f"Chart successfully saved as '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving the chart for {ticker}: {e}")
