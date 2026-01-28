import time
from datetime import datetime
from .api_client import AlphaVantageClient
from .database import get_session, Asset, DailyPrice

def run_etl():
    """
    Core ETL process:
    1. Extract tickers from 'asset' table.
    2. Fetch latest data via API with a safety delay to avoid rate limits.
    3. Load data into 'daily_price', avoiding duplicates.
    """
    session = get_session()
    client = AlphaVantageClient()
    
    # 1. Extract: Get all tracked assets
    assets = session.query(Asset).all()
    
    if not assets:
        print("No assets found in the database. Please add some first.")
        session.close()
        return

    for asset in assets:
        print(f"Processing {asset.ticker_symbol}...")
        raw_data = client.get_daily_data(asset.ticker_symbol)
        
        # Enhanced Error Diagnosis
        if not raw_data or "Time Series (Daily)" not in raw_data:
            # Captures specific API messages (e.g., rate limit notes or invalid symbols)
            error_reason = "Unknown error"
            if raw_data:
                error_reason = raw_data.get("Note") or raw_data.get("Error Message") or "Data key missing"
            
            print(f"Failed to fetch data for {asset.ticker_symbol}: {error_reason}")
            continue
            
        time_series = raw_data["Time Series (Daily)"]
        
        # 3. Load: Save new records
        new_records_count = 0
        for date_str, values in time_series.items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if record already exists to maintain data integrity
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

        # Cooldown: Sleep for 15 seconds to respect Alpha Vantage free tier limits
        # (5 requests per minute / 60 seconds = 1 request every 12 seconds)
        print("Waiting 15 seconds for API cooldown...")
        time.sleep(15)
    
    session.close()
