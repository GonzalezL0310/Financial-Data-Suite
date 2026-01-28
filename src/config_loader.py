import os
from .database import get_session, Asset

def sync_assets_from_config(file_path="tickers.txt"):
    """
    Reads tickers from a text file and ensures they exist in the database.
    If a ticker is in the file but not in the DB, it adds it.
    """
    if not os.path.exists(file_path):
        print(f"Warning: Configuration file '{file_path}' not found.")
        return []

    # Read tickers from file
    with open(file_path, "r") as f:
        # Clean whitespace and filter out empty lines
        tickers = [line.strip().upper() for line in f if line.strip()]

    session = get_session()
    new_assets_count = 0
    
    for ticker in tickers:
        # Check if asset already exists to avoid duplicates
        exists = session.query(Asset).filter_by(ticker_symbol=ticker).first()
        if not exists:
            # For now, we use the ticker as the name if unknown
            new_asset = Asset(ticker_symbol=ticker, asset_name=f"{ticker} (Auto-added)")
            session.add(new_asset)
            new_assets_count += 1
    
    session.commit()
    session.close()
    
    if new_assets_count > 0:
        print(f"Sync complete: Added {new_assets_count} new assets to the database.")
    
    return tickers
