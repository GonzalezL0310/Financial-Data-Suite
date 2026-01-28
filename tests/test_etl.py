import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, Asset, DailyPrice
from src.etl_engine import run_etl

# Setup an in-memory database for testing
@pytest.fixture
def temp_db():
    """Creates a fresh, in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@patch('src.etl_engine.get_session')
@patch('src.etl_engine.AlphaVantageClient')
def test_run_etl_inserts_data(mock_client_class, mock_get_session, temp_db):
    """
    Verifies that the ETL correctly parses API data and inserts it into the DB.
    """
    # 1. Setup Mock Session and Client
    mock_get_session.return_value = temp_db
    mock_instance = mock_client_class.return_value
    
    # 2. Seed the temporary DB with an asset
    asset = Asset(ticker_symbol="AAPL", asset_name="Apple Inc.")
    temp_db.add(asset)
    temp_db.commit()

    # 3. Simulate a successful API response
    mock_instance.get_daily_data.return_value = {
        "Time Series (Daily)": {
            "2024-01-01": {
                "1. open": "150.00", "2. high": "155.00", 
                "3. low": "149.00", "4. close": "152.00", "5. volume": "1000"
            }
        }
    }

    # 4. Execute the ETL
    run_etl()

    # 5. Assertions: Verify the data was saved correctly [cite: 97]
    saved_price = temp_db.query(DailyPrice).filter_by(asset_id=asset.id).first()
    assert saved_price is not None
    assert saved_price.close == 152.00
    assert saved_price.volume == 1000
