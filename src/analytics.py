import pandas as pd
import numpy as np
from .config_loader import settings
from .database import get_session, DailyPrice, Asset

def load_data_from_db(ticker: str):
    """Fetches historical data from the database for a specific ticker."""
    session = get_session()
    
    # Buscamos el activo
    asset = session.query(Asset).filter_by(ticker_symbol=ticker.strip().upper()).first()
    
    if not asset:
        session.close()
        return None
        
    # Obtenemos los registros de precios directamente
    prices_query = session.query(DailyPrice).filter_by(asset_id=asset.id).order_by(DailyPrice.date.asc())
    prices = prices_query.all()
    
    session.close() # Cerramos la sesión rápido para liberar la DB
    
    if not prices:
        return None
        
    # Convertimos la lista de objetos SQLAlchemy a un DataFrame de Pandas de forma limpia
    data = [
        {
            "date": p.date,
            "open": p.open,
            "high": p.high,
            "low": p.low,
            "close": p.close,
            "volume": p.volume
        } for p in prices
    ]
    
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    return df

def calculate_metrics(df: pd.DataFrame):
    """
    Calcula métricas usando operaciones vectorizadas de alto rendimiento.
    """
    df = df.copy()

    # Parámetros desde settings (Adiós números mágicos)
    s_p = settings['analytics']['sma_short']
    l_p = settings['analytics']['sma_long']
    rsi_p = settings['analytics']['rsi_period']
    bb_p = settings['analytics']['bollinger_period']
    bb_std = settings['analytics']['bollinger_std']

    # Vectorización pura: Pandas opera sobre toda la columna a la vez
    df['returns'] = df['close'].pct_change()
    df['sma_short'] = df['close'].rolling(window=s_p).mean()
    df['sma_long'] = df['close'].rolling(window=l_p).mean()

    # RSI Vectorizado con EWMA (Más rápido y preciso)
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=rsi_p - 1, min_periods=rsi_p).mean()
    avg_loss = loss.ewm(com=rsi_p - 1, min_periods=rsi_p).mean()

    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Bandas de Bollinger Vectorizadas
    df['bb_mid'] = df['close'].rolling(window=bb_p).mean()
    df['bb_std'] = df['close'].rolling(window=bb_p).std()
    df['bb_upper'] = df['bb_mid'] + (df['bb_std'] * bb_std)
    df['bb_lower'] = df['bb_mid'] - (df['bb_std'] * bb_std)

    return df
