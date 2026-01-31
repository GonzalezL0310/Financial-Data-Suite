# Financial Data Suite: Unified Quantitative Analytics Engine

This project is a comprehensive financial engineering ecosystem designed to bridge the gap between raw market data and actionable quantitative insights. It integrates automated ETL (Extract, Transform, Load) pipelines, relational data persistence, and high-performance risk modeling into a unified system accessible via a REST API.

## Current Features (Phase 1 - 4)

The system currently implements a modular architecture that covers the full data lifecycle:

- Automated ETL Engine: A robust extraction process that synchronizes multi-asset historical data from the Alpha Vantage API. It includes safety mechanisms like API cooldown handling and duplicate record prevention.
-  Relational Persistence: Uses SQLAlchemy ORM and SQLite with Write-Ahead Logging (WAL) for high-concurrency data management.
- Quant Analytics Core: High-performance vectorized calculations for technical indicators, including:
 - Trend: Simple Moving Averages (SMA).
 - Momentum: Vectorized Relative Strength Index (RSI) using EWMA.
 - Volatility: Standard deviation and Bollinger Bands.
-  Risk Modeling Module: Implementation of professional risk metrics:
 - Value at Risk (VaR): Parametric (Variance-Covariance) and Historical methodologies.
 - Monte Carlo Simulation: 1,000+ simulations to project potential future price paths and extreme market scenarios.
- Service Layer (FastAPI): A modern REST API that exposes backtesting results, risk analytics, and technical indicators in real-time.
- Software Standards: Dynamic configuration via settings.yaml, environment isolation (.env), and automated data integrity validation.

## Tech Stack

- Languages: Python 3.12+.
- Data Science: Pandas, NumPy, SciPy.
- Engineering: FastAPI, SQLAlchemy, Uvicorn.
- Configuration: YAML, Python-Dotenv.
- Testing: Pytest.

## Future Roadmap (Phase 5+)

Based on the project's evolution plan, the following features are currently in development:

- Vectorized Backtester Optimization: Implementing Numba (JIT) and Cython to achieve 100-1000x faster execution for complex signal logic.
- Econometric Validation: Integration of Statsmodels for formal statistical testing, including Cointegration and Stationarity (Project 5).
- Advanced Portfolio Theory: Transitioning from single-asset risk to Markowitz Portfolio Optimization and multi-asset correlation matrices.
- Database Scalability: Migrating the local SQLite storage to a production-grade PostgreSQL instance.

## Setup & Execution
1. Prerequisites
Ensure you have Python 3 installed and an active Alpha Vantage API Key.

2. Automated Installation
The provided setup script automates environment creation and dependency management:
```Bash
# Clone the repository
git clone <your-repo-url>
cd financial-data-suite

# Run the setup script
chmod +x setup.sh
./setup.sh
```

3. Configuration
Add your API key to the generated .env file:
```Bash
ALPHA_VANTAGE_API_KEY=your_real_key_here
```

Modify tickers.txt to include the assets you wish to track.

4. Running the System
You can run the full analytical suite or just the API server:
```Bash
# Activate environment
source venv/bin/activate

# Option A: Run Full ETL + Analysis
python main.py

# Option B: Launch REST API Server
python main.py --api
```
