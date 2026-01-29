import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .config_loader import settings

# Get the absolute path of the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, settings['system']['data_directory'])
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, settings['system']['database_name'])}"

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Using modern declarative_base to avoid MovedIn20Warning
Base = declarative_base()

class Asset(Base):
    """
    Represents a financial instrument (e.g., AAPL, TSLA).
    Contains static information.
    """
    __tablename__ = 'asset'
    
    id = Column(Integer, primary_key=True)
    ticker_symbol = Column(String, unique=True, nullable=False)
    asset_name = Column(String, nullable=False)
    
    # Relationship to link prices to this asset
    prices = relationship("DailyPrice", back_populates="asset", cascade="all, delete-orphan")

class DailyPrice(Base):
    """
    Stores daily OHLCV (Open, High, Low, Close, Volume) data.
    """
    __tablename__ = 'daily_price'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    
    asset = relationship("Asset", back_populates="prices")

def get_session():
    """
    Creates and returns a new database session.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    """
    Initializes the database and creates the tables.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
