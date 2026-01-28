import os
import sys

# Add the project root to sys.path to allow running this script directly
# This ensures that 'from src.database' works by looking at the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_session, DailyPrice

def validate_data():
    """
    Validates the coherence and integrity of the stored market data.
    Checks for logical price anomalies (High >= Low) and non-positive values.
    """
    session = get_session()
    prices = session.query(DailyPrice).all()
    errors = 0

    print(f"--- Validating {len(prices)} records ---")
    
    for p in prices:
        # Logical check: High must be greater than or equal to Low, Open, and Close
        if not (p.high >= p.low and p.high >= p.open and p.high >= p.close):
            print(f"Anomaly detected: Asset ID {p.asset_id} on {p.date}")
            print(f"  Details: O:{p.open} H:{p.high} L:{p.low} C:{p.close}")
            errors += 1
        
        # Physical check: Prices and volume must be positive
        if any(val <= 0 for val in [p.open, p.high, p.low, p.close]) or p.volume < 0:
            print(f"Invalid value detected: Asset ID {p.asset_id} on {p.date}")
            errors += 1

    session.close()
    
    if errors == 0:
        print("Verification finished: Data is coherent and clean.")
    else:
        print(f"Verification finished: {errors} anomalies found in the database.")

if __name__ == "__main__":
    validate_data()
