from test import IBDataFetcher

def get_basic_stock_data():
    """Basic examples of getting stock data"""
    fetcher = IBDataFetcher(port=4002)  # Using paper trading
    try:
        # Get current data
        df = fetcher.get_historical_data(
            symbol='SPY',
            duration='1 Y',
            bar_size='1 hour',
            output_name='spy_current',
            output_dir='data/basic'
        )
        
        # Get historical data
        df_historical = fetcher.get_historical_data(
            symbol='SPY',
            duration='1 Y',
            bar_size='1 hour',
            end_datetime='20231231 16:00:00',  # End at market close
            output_name='spy_2023',
            output_dir='data/basic'
        )
        
        return {
            'current': df,
            'historical': df_historical
        }
    finally:
        fetcher.disconnect()

if __name__ == "__main__":
    # Create data directory
    import os
    os.makedirs('data/basic', exist_ok=True)
    
    print("Getting basic stock data examples...")
    data = get_basic_stock_data()
    for name, df in data.items():
        if df is not None:
            print(f"\n{name} data:")
            print(df.head())
