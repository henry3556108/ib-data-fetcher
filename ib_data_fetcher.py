from ib_insync import *
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Union, Optional

class IBDataFetcher:
    """Interactive Brokers data fetcher class"""
    
    # Valid parameter values based on IB API documentation
    VALID_DURATIONS = ['S', 'D', 'W', 'M', 'Y']
    
    # Bar sizes exactly as specified in IB API documentation
    VALID_BAR_SIZES = [
        # Seconds
        '1 secs', '5 secs', '10 secs', '15 secs', '30 secs',
        # Minutes
        '1 min', '2 mins', '3 mins', '5 mins', '10 mins', 
        '15 mins', '20 mins', '30 mins',
        # Hours
        '1 hour', '2 hours', '3 hours', '4 hours', '8 hours',
        # Days and above
        '1 day', '1 week', '1 month'
    ]
    
    # Data types with their restrictions
    VALID_WHAT_TO_SHOW = {
        'TRADES': 'Default. Adjusted for splits but not dividends',
        'BID': 'Bid data',
        'ASK': 'Ask data',
        'MIDPOINT': 'Midpoint data, good for forex',
        'BID_ASK': 'Bid and ask prices',
        'ADJUSTED_LAST': 'Adjusted for both splits and dividends. TWS 967+ only',
        'SCHEDULE': 'Trading schedule, 1 day bars only. TWS API 10.12+ only',
        'AGGTRADES': 'For crypto contracts only'
    }

    def __init__(self, host: str = '127.0.0.1', port: int = 4001, client_id: int = 123):
        """
        Initialize the IBDataFetcher
        
        Parameters:
        -----------
        host : str
            IB Gateway/TWS host address
        port : int
            IB Gateway/TWS port (4001 for live, 4002 for paper)
        client_id : int
            Unique client ID for the connection
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = None
    
    def connect(self) -> bool:
        """Connect to Interactive Brokers"""
        try:
            self.ib = IB()
            self.ib.connect(self.host, self.port, self.client_id)
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from Interactive Brokers"""
        if self.ib and self.ib.isConnected():
            self.ib.disconnect()
    
    def _validate_parameters(self, duration: str, bar_size: str, what_to_show: str):
        """
        Validate input parameters according to IB API restrictions
        
        Raises:
        -------
        ValueError: If any parameter is invalid or violates IB API restrictions
        """
        # Parse duration unit
        try:
            unit = duration.strip()[-1].upper()
        except (ValueError, IndexError):
            raise ValueError(f"Invalid duration format. Must be like '1 Y', '6 M', etc.")
            
        # Validate duration unit
        if unit not in self.VALID_DURATIONS:
            raise ValueError(f"Invalid duration unit. Must end with one of {self.VALID_DURATIONS}")
        
        # Check bar size
        if bar_size not in self.VALID_BAR_SIZES:
            raise ValueError(f"Invalid bar size. Must be one of {self.VALID_BAR_SIZES}")
        
        # Check what to show
        if what_to_show not in self.VALID_WHAT_TO_SHOW:
            raise ValueError(f"Invalid what_to_show. Must be one of {list(self.VALID_WHAT_TO_SHOW.keys())}")
            
        # Special restrictions for what_to_show
        if what_to_show == 'SCHEDULE' and bar_size != '1 day':
            raise ValueError("SCHEDULE data only available with '1 day' bar size")
        if what_to_show == 'AGGTRADES' and not isinstance(self.contract, Crypto):
            raise ValueError("AGGTRADES only available for crypto contracts")

    def get_historical_data(
        self,
        symbol: str,
        duration: str = '1 Y',
        bar_size: str = '1 hour',
        output_name: Optional[str] = None,
        output_dir: Optional[str] = None,
        exchange: str = 'SMART',
        currency: str = 'USD',
        what_to_show: str = 'TRADES',
        use_rth: bool = True,
        end_datetime: str = ''
    ) -> Union[pd.DataFrame, None]:
        """
        Get historical data from Interactive Brokers
        
        Parameters:
        -----------
        symbol : str
            Stock symbol (e.g., 'SPY', 'AAPL')
        duration : str
            Time duration (e.g., '1 Y', '6 M', '10 D')
            Valid units: S (Seconds), D (Day), W (Week), M (Month), Y (Year)
        bar_size : str
            Size of each bar. Valid sizes:
            - Seconds: 1, 5, 10, 15, 30 secs
            - Minutes: 1, 2, 3, 5, 10, 15, 20, 30 mins
            - Hours: 1, 2, 3, 4, 8 hours
            - Days+: 1 day, 1 week, 1 month
        output_name : str, optional
            Name of output CSV file (without .csv extension)
            If None, will use {symbol}_{duration}_{bar_size}.csv
        output_dir : str, optional
            Directory to save the CSV file
            If None, saves in current directory
        exchange : str
            Exchange name (default: 'SMART')
        currency : str
            Currency code (default: 'USD')
        what_to_show : str
            Type of data to show (default: 'TRADES')
            See VALID_WHAT_TO_SHOW for all options and restrictions
        use_rth : bool
            Use Regular Trading Hours only (default: True)
        end_datetime : str
            End date and time for the data request (default: '')
            Format: 'YYYYMMDD HH:mm:ss' or '' for current time
            Examples: '20200101 15:59:00', '20231231 16:00:00'
        
        Returns:
        --------
        pd.DataFrame or None
            DataFrame containing the historical data, None if error occurs
        """
        try:
            # Validate parameters
            self._validate_parameters(duration, bar_size, what_to_show)
            
            # Connect if not already connected
            if not self.ib or not self.ib.isConnected():
                if not self.connect():
                    return None
            
            # Create contract
            contract = Stock(symbol, exchange, currency)
            
            # Request historical data
            print(f"Requesting {duration} of {bar_size} data for {symbol}...")
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime=end_datetime,
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow=what_to_show,
                useRTH=use_rth,
                formatDate=1
            )
            
            if not bars:
                print("No data received")
                return None
                
            print(f"Received {len(bars)} bars")
            
            # Convert to DataFrame
            data = []
            for bar in bars:
                data.append({
                    'date': bar.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'open': bar.open,
                    'high': bar.high,
                    'low': bar.low,
                    'close': bar.close,
                    'volume': bar.volume,
                    'average': bar.average,
                    'barCount': bar.barCount
                })
            
            df = pd.DataFrame(data)
            
            # Save to CSV if output_name is provided or generate default name
            if output_name is not None or output_dir is not None:
                if output_name is None:
                    output_name = f"{symbol}_{duration.replace(' ', '')}_{bar_size.replace(' ', '')}"
                
                if output_dir is not None:
                    os.makedirs(output_dir, exist_ok=True)
                    csv_path = os.path.join(output_dir, f"{output_name}.csv")
                else:
                    csv_path = f"{output_name}.csv"
                
                df.to_csv(csv_path, index=False)
                print(f"Data saved to {csv_path}")
            
            return df
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

# Example usage:
if __name__ == "__main__":
    # Create data fetcher instance
    fetcher = IBDataFetcher(port=4001)  # Use 4001 for live, 4002 for paper trading
    
    try:
        # Get SPY data for last 3 years with 30-min bars
        df_spy = fetcher.get_historical_data(
            symbol='SPY',
            duration='3 Y',
            bar_size='30 mins',
            output_name='spy_3y_30m_v2',
            output_dir='data'  # Will create a 'data' directory if it doesn't exist
        )
        
        if df_spy is not None:
            print("\nFirst few rows of data:")
            print(df_spy.head())
            print("\nDataFrame Info:")
            print(df_spy.info())
            
    finally:
        # Always disconnect when done
        fetcher.disconnect()