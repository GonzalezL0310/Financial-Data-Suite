import pandas as pd
from .database import get_session, DailyPrice, Asset

def load_data_from_db(ticker: str):
    """Fetches historical data from the database for a specific ticker."""
    session = get_session()
    asset = session.query(Asset).filter_by(ticker_symbol=ticker).first()
    
    if not asset:
        session.close()
        return None
        
    query = session.query(DailyPrice).filter_by(asset_id=asset.id).order_by(DailyPrice.date.asc())
    df = pd.read_sql(query.statement, session.bind)
    session.close()
    
    if df.empty:
        return None
        
    df.set_index('date', inplace=True)
    return df

def calculate_metrics(df: pd.DataFrame, short_sma=50, long_sma=200):
    """Calculates returns, SMAs, and volatility."""
    df = df.copy()
    df['returns'] = df['close'].pct_change()
    df['sma_short'] = df['close'].rolling(window=short_sma).mean()
    df['sma_long'] = df['close'].rolling(window=long_sma).mean()
    df['volatility'] = df['returns'].rolling(window=30).std()
    return df
