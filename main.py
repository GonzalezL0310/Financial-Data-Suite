import os
import sys
import uvicorn
from src.database import init_db
from src.etl_engine import run_etl
from src.analytics import load_data_from_db, calculate_metrics
from src.visualizer import plot_metrics
from src.config_loader import sync_assets_from_config

def check_env_file():
    """Validates that the .env file exists and contains a real key."""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key or api_key == "your_key_here":
        print("\n" + "!"*50)
        print("ERROR: Invalid API Key in .env file.")
        print("!"*50 + "\n")
        return False
    return True

def analyze_and_plot(ticker: str):
    """Handles analysis and visualization for a single ticker."""
    print(f"\n>>> Analyzing: {ticker}")
    df = load_data_from_db(ticker)
    if df is not None:
        df_metrics = calculate_metrics(df)
        plot_metrics(df_metrics, ticker, 'close', 'sma_short', 'sma_long')
    else:
        print(f"Warning: No data for {ticker} found in database. Run ETL first.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        print("--- Lanzando Servidor API ---")
        uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)  
    
    else:
        # 1. System Setup
        init_db()
    
        # 2. Sync DB with Tickers Config File
        print("--- Phase 0: Syncing Configuration ---")
        active_tickers = sync_assets_from_config("tickers.txt")
    
        if check_env_file() and active_tickers:
            print("\n--- Phase 1: Global Data Synchronization ---")
            run_etl(ticker_list=active_tickers)
        
            print("\n--- Phase 2: Quantitative Analysis ---")
            for t in active_tickers:
                analyze_and_plot(t)
    
        print("\n--- All operations completed ---")
