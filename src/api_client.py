import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AlphaVantageClient:
    """
    Client to interact with Alpha Vantage API.
    Handles data extraction for the ETL pipeline.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key missing. Please set ALPHA_VANTAGE_API_KEY in .env")

    def get_daily_data(self, symbol: str):
        """
        Fetches daily adjusted prices for a given ticker symbol.
        Returns the raw JSON response or raises an exception on failure.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "compact"  # Last 100 data points
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Basic error handling for Alpha Vantage specific messages
            if "Error Message" in data:
                raise ValueError(f"Invalid symbol: {symbol}")
            if "Note" in data:
                raise Exception("API rate limit reached.")

            return data
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return None

if __name__ == "__main__":
    # Quick test execution
    client = AlphaVantageClient()
    print(client.get_daily_data("AAPL"))
