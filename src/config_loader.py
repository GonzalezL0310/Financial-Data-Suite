import os
import yaml

def load_settings(file_path="settings.yaml"):
    """Carga la configuración global desde un archivo YAML."""
    if not os.path.exists(file_path):
        # Valores por defecto de seguridad
        return {
            "system": {"database_name": "market_data.db", "data_directory": "data", "tickers_file": "tickers.txt"},
            "etl": {"api_cooldown_seconds": 15, "output_size": "full"},
            "analytics": {"sma_short": 50, "sma_long": 200, "rsi_period": 14, "bollinger_period": 20, "bollinger_std": 2, "volatility_window": 30},
            "visualizer": {"output_dir": "metrics", "figure_size": [12, 6], "line_alpha": 0.8},
            "api": {"host": "127.0.0.1", "port": 8000}
        }
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# Instancia global disponible para todo el proyecto
settings = load_settings()

def sync_assets_from_config(file_path=None):
    """
    Sincroniza tickers. Importa la base de datos de forma local para evitar 
    importaciones circulares.
    """
    # IMPORTACIÓN LOCAL: Rompe el ciclo con database.py
    from .database import get_session, Asset 

    if file_path is None:
        file_path = settings['system']['tickers_file']

    if not os.path.exists(file_path):
        print(f"Warning: Configuration file '{file_path}' not found.")
        return []

    with open(file_path, "r") as f:
        tickers = [line.strip().upper() for line in f if line.strip()]

    session = get_session()
    new_assets_count = 0
    
    for ticker in tickers:
        exists = session.query(Asset).filter_by(ticker_symbol=ticker).first()
        if not exists:
            new_asset = Asset(ticker_symbol=ticker, asset_name=f"{ticker} (Auto-added)")
            session.add(new_asset)
            new_assets_count += 1
    
    session.commit()
    session.close()
    
    if new_assets_count > 0:
        print(f"Sync complete: Added {new_assets_count} new assets to the database.")
    
    return tickers
