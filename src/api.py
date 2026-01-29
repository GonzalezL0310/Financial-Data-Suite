from fastapi import FastAPI, HTTPException
from .analytics import load_data_from_db
from .strategies import run_crossover_strategy

app = FastAPI(title="Financial Data Suite API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Suite Financiera lista para operar"}

@app.get("/backtest/{ticker}")
def get_backtest(ticker: str, short: int = 50, long: int = 200):
    """
    Ejecuta un backtest para un ticker específico usando datos de la base de datos.
    """
    # Cargamos datos usando el módulo de analytics que ya tenemos
    df = load_data_from_db(ticker.upper())
    
    if df is None:
        raise HTTPException(status_code=404, detail=f"No hay datos para el ticker {ticker} en la base de datos.")
    
    results = run_crossover_strategy(df, short, long)
    
    if "error" in results:
        raise HTTPException(status_code=400, detail=results["error"])
        
    return {
        "ticker": ticker.upper(),
        "params": {"short_mva": short, "long_mva": long},
        "results": results
    }

@app.get("/analytics/{ticker}")
def get_full_analytics(ticker: str):
    """
    Retorna el último estado de todos los indicadores técnicos para un ticker.
    """
    df = load_data_all(ticker.upper()) # Función que carga de la DB
    if df is None:
        raise HTTPException(status_code=404, detail="Ticker no encontrado")
    
    full_df = calculate_metrics(df)
    last_row = full_df.iloc[-1] # Tomamos solo el dato más reciente
    
    return {
        "ticker": ticker.upper(),
        "date": str(full_df.index[-1]),
        "price": round(last_row['close'], 2),
        "indicators": {
            "rsi": round(last_row['rsi'], 2),
            "volatility": round(last_row['volatility'], 4),
            "bollinger": {
                "upper": round(last_row['bb_upper'], 2),
                "mid": round(last_row['bb_mid'], 2),
                "lower": round(last_row['bb_lower'], 2)
            }
        }
    }
