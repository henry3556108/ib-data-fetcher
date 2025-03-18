from test import IBDataFetcher

def get_multiple_stocks():
    """Example of getting data for multiple stocks"""
    fetcher = IBDataFetcher(port=4002)  # Using paper trading
    try:
        stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        dfs = {}
        
        for symbol in stocks:
            print(f"\nFetching data for {symbol}")
            # Get current data
            df_current = fetcher.get_historical_data(
                symbol=symbol,
                duration='1 Y',
                bar_size='1 day',
                output_name=f'{symbol.lower()}_current',
                output_dir='data/stocks'
            )
            
            # Get 2023 data
            df_2023 = fetcher.get_historical_data(
                symbol=symbol,
                duration='1 Y',
                bar_size='1 day',
                end_datetime='20231231 16:00:00',  # End at market close
                output_name=f'{symbol.lower()}_2023',
                output_dir='data/stocks'
            )
            
            dfs[f'{symbol}_current'] = df_current
            dfs[f'{symbol}_2023'] = df_2023
            
        return dfs
    finally:
        fetcher.disconnect()

def get_market_data_types():
    """Example of different market data types"""
    fetcher = IBDataFetcher(port=4002)
    try:
        data_types = {}
        
        # Get trades data (default)
        data_types['trades'] = fetcher.get_historical_data(
            symbol='SPY',
            duration='1 D',
            bar_size='5 mins',
            what_to_show='TRADES',
            output_name='spy_trades',
            output_dir='data/types'
        )
        
        # Get bid-ask data
        data_types['bid_ask'] = fetcher.get_historical_data(
            symbol='SPY',
            duration='1 D',
            bar_size='5 mins',
            what_to_show='BID_ASK',
            output_name='spy_bidask',
            output_dir='data/types'
        )
        
        # Get adjusted last price
        data_types['adjusted'] = fetcher.get_historical_data(
            symbol='SPY',
            duration='1 M',
            bar_size='1 day',
            what_to_show='ADJUSTED_LAST',
            output_name='spy_adjusted',
            output_dir='data/types'
        )
        
        return data_types
    finally:
        fetcher.disconnect()

if __name__ == "__main__":
    # Create data directories
    import os
    for dir_name in ['stocks', 'types']:
        os.makedirs(f'data/{dir_name}', exist_ok=True)
    
    print("Getting multiple stocks data...")
    stock_data = get_multiple_stocks()
    for name, df in stock_data.items():
        if df is not None:
            print(f"\n{name} data:")
            print(df.head())
    
    print("\nGetting different market data types...")
    type_data = get_market_data_types()
    for name, df in type_data.items():
        if df is not None:
            print(f"\n{name} data:")
            print(df.head())
