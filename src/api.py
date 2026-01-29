from fastapi import FastAPI, HTTPException
import pandas as pd
from .strategies import run_crossover_strategy
from .analytics import load_data_from_db, calculate_metrics
from .quant_analysis import calculate_var_parametric, calculate_var_historical, run_monte_carlo_simulation
from .config_loader import settings

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
    df = load_data_from_db(ticker.upper()) # Función que carga de la DB
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

@app.get("/risk/{ticker}")
def get_risk_analysis(ticker: str):
    df = load_data_from_db(ticker.upper())
    if df is None:
        raise HTTPException(status_code=404, detail="Ticker no encontrado")
    
    # Necesitamos los retornos para el cálculo de riesgo
    returns = df['close'].pct_change().dropna()
    last_price = float(df['close'].iloc[-1])
    
    var_p = calculate_var_parametric(returns)
    var_h = calculate_var_historical(returns)
    mc_results = run_monte_carlo_simulation(last_price, returns)
    
    return {
        "ticker": ticker.upper(),
        "value_at_risk_pct": {
            "parametric": var_p,
            "historical": var_h,
            "monte_carlo": mc_results["var_monte_carlo_pct"]
        },
        "monte_carlo_projections": {
            "days_ahead": settings['risk_management']['monte_carlo_days'],
            "expected_avg_price": mc_results["expected_price_avg"],
            "extreme_scenarios": [
                mc_results["min_potential_price"], 
                mc_results["max_potential_price"]
            ]
        }
    }
