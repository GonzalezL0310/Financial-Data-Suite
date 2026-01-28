from src.database import get_session, Asset
from src.etl_engine import run_etl

def initialize_demo_assets():
    """Initializes the database with some tickers if empty."""
    session = get_session()
    if session.query(Asset).count() == 0:
        demo_assets = [
            Asset(ticker_symbol="AAPL", asset_name="Apple Inc."),
            Asset(ticker_symbol="MSFT", asset_name="Microsoft Corp.")
        ]
        session.add_all(demo_assets)
        session.commit()
    session.close()

if __name__ == "__main__":
    print("--- Starting Market Data Pipeline ---")
    initialize_demo_assets()
    run_etl()
    print("--- Pipeline Execution Finished ---")
