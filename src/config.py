"""
Configuration Module

Stores all global constants and parameters to facilitate 
adjustments and avoid magic numbers.
"""

# --- Acquisition Parameters ---
TICKER_SYMBOL: str = "SPY"
DATA_PERIOD: str = "5y"

# --- Processing Parameters ---
SHORT_SMA_PERIOD: int = 50
LONG_SMA_PERIOD: int = 200
VOLATILITY_PERIOD: int = 30
