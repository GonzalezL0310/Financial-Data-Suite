import pandas as pd
import numpy as np

def run_crossover_strategy(df: pd.DataFrame, short_window: int = 50, long_window: int = 200):
    """
    Calcula el rendimiento de una estrategia de cruce de medias.
    """
    if len(df) < long_window:
        return {"error": f"Datos insuficientes. Se requieren al menos {long_window} registros."}

    data = df.copy()
    
    # 1. Señales (ya calculadas o las recalculamos para asegurar flexibilidad)
    data['sma_s'] = data['close'].rolling(window=short_window).mean()
    data['sma_l'] = data['close'].rolling(window=long_window).mean()
    
    # 2. Lógica de Posición: 1 (Comprado), 0 (Fuera del mercado)
    data['position'] = np.where(data['sma_s'] > data['sma_l'], 1, 0)
    
    # 3. Cálculo de Retornos
    data['market_log_ret'] = np.log(data['close'] / data['close'].shift(1))
    data['strategy_ret'] = data['position'].shift(1) * data['market_log_ret']
    
    # 4. Rendimiento Acumulado
    cum_market = np.exp(data['market_log_ret'].sum()) - 1
    cum_strategy = np.exp(data['strategy_ret'].sum()) - 1
    
    return {
        "market_return_pct": round(cum_market * 100, 2),
        "strategy_return_pct": round(cum_strategy * 100, 2),
        "performance_vs_market": round((cum_strategy - cum_market) * 100, 2),
        "total_days": len(data)
    }
