import time
from .config_loader import settings
from datetime import datetime
from .api_client import AlphaVantageClient
from .database import get_session, Asset, DailyPrice

def run_etl(ticker_list=None):
    """
    Core ETL process:
    1. Extract tickers from 'asset' table.
    2. Fetch LATEST FULL data via API with safety delays.
    3. Load data into 'daily_price', avoiding duplicates.
    """
    session = get_session()
    client = AlphaVantageClient()
    cooldown = settings['etl']['api_cooldown_seconds']
    out_size = settings['etl']['output_size']

    if ticker_list:
        assets = session.query(Asset).filter(Asset.ticker_symbol.in_(ticker_list)).all()
    else:
        assets = session.query(Asset).all()

    if not assets:
        print("No assets found in the database. Please add some first.")
        session.close()
        return

    for asset in assets:
        print(f"Processing {asset.ticker_symbol}...")
        
        # FIX 1: Explicitly request 'full' to get more than 100 records
        raw_data = client.get_daily_data(asset.ticker_symbol, outputsize=out_size)
        
        # FIX 2: Enhanced Error Diagnosis & Flow Control
        if not raw_data or "Time Series (Daily)" not in raw_data:
            # Captures specific API messages or provides a fallback string
            error_reason = "Unknown API response format"
            if raw_data:
                error_reason = raw_data.get("Note") or raw_data.get("Error Message") or raw_data.get("Information") or "Data key missing"
            
            print(f"Skipping {asset.ticker_symbol}: {error_reason}")
            
            if raw_data and "Note" in raw_data:
                print("Rate limit reached. Safety cooldown of",cooldown,"s...")
                time.sleep(cooldown)
            
            continue
            
        time_series = raw_data["Time Series (Daily)"]
        
        # 3. Load: Save new records
        new_records_count = 0
        for date_str, values in time_series.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if record already exists
            exists = session.query(DailyPrice).filter_by(
                asset_id=asset.id, date=date_obj
            ).first()
            
            if not exists:
                new_price = DailyPrice(
                    asset_id=asset.id,
                    date=date_obj,
                    open=float(values["1. open"]),
                    high=float(values["2. high"]),
                    low=float(values["3. low"]),
                    close=float(values["4. close"]),
                    volume=int(values["5. volume"])
                )
                session.add(new_price)
                new_records_count += 1
        
        session.commit()
        print(f"Finished updating {asset.ticker_symbol}. Added {new_records_count} new records.")

        # Standard Cooldown
        print("Waiting",cooldown,"seconds for API cooldown...")
        time.sleep(cooldown)
    
    session.close()
