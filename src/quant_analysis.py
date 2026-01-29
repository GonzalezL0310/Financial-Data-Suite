import numpy as np
from .config_loader import settings

def calculate_var_parametric(returns):
    """VaR Paramétrico (Varianza-Covarianza). Asume distribución normal."""
    conf = settings['risk_management']['var_confidence_level']
    mu = returns.mean()
    sigma = returns.std()
    from scipy.stats import norm
    var = norm.ppf(1 - conf, mu, sigma)
    return round(var * 100, 2)

def calculate_var_historical(returns):
    """VaR Histórico. Basado en el percentil real de los datos pasados."""
    conf = settings['risk_management']['var_confidence_level']
    var = np.percentile(returns.dropna(), (1 - conf) * 100)
    return round(var * 100, 2)

def run_monte_carlo_simulation(last_price, returns):
    """Simulación de Monte Carlo para proyectar precios futuros."""
    n_sims = settings['risk_management']['monte_carlo_simulations']
    n_days = settings['risk_management']['monte_carlo_days']
    
    # Vectorización: Generamos una matriz (días x simulaciones) de golpe
    # Evitamos miles de iteraciones en Python
    periodic_ret = np.random.normal(returns.mean(), returns.std(), (n_days, n_sims))
    
    # np.cumprod opera sobre el eje de los días de forma paralela
    price_paths = last_price * (1 + periodic_ret).cumprod(axis=0)
    
    final_prices = price_paths[-1]

    # VaR por Monte Carlo (basado en el último día de la simulación)
    final_prices = price_paths[-1]
    returns_sim = (final_prices / last_price) - 1
    conf = settings['risk_management']['var_confidence_level']
    var_mc = np.percentile(returns_sim, (1 - conf) * 100)
    
    return {
        "expected_price_avg": round(float(final_prices.mean()), 2),
        "max_potential_price": round(float(final_prices.max()), 2),
        "min_potential_price": round(float(final_prices.min()), 2),
        "var_monte_carlo_pct": round(float(var_mc * 100), 2)
    }
