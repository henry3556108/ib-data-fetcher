from ib_data_fetcher import IBDataFetcher

def get_forex_data():
    """Examples of getting forex data"""
    fetcher = IBDataFetcher(port=4002)  # Using paper trading
    try:
        # Get current EUR.USD hourly data
        eurusd_current = fetcher.get_historical_data(
            symbol='EUR',
            exchange='IDEALPRO',  # Important: use IDEALPRO for forex
            currency='USD',
            duration='1 W',
            bar_size='1 hour',
            what_to_show='MIDPOINT',  # Important: use MIDPOINT for forex
            output_name='eurusd_current',
            output_dir='data/forex'
        )
        
        # Get historical EUR.USD hourly data
        eurusd_historical = fetcher.get_historical_data(
            symbol='EUR',
            exchange='IDEALPRO',
            currency='USD',
            duration='1 W',
            bar_size='1 hour',
            what_to_show='MIDPOINT',
            end_datetime='20240101 00:00:00',  # Start of 2024
            output_name='eurusd_historical',
            output_dir='data/forex'
        )
        
        return {
            'EUR.USD_current': eurusd_current,
            'EUR.USD_historical': eurusd_historical
        }
    finally:
        fetcher.disconnect()

def get_crypto_data():
    """Examples of getting crypto data"""
    fetcher = IBDataFetcher(port=4002)
    try:
        # Get current Bitcoin data
        btc_current = fetcher.get_historical_data(
            symbol='BTC',
            exchange='PAXOS',
            currency='USD',
            duration='1 D',
            bar_size='5 mins',
            what_to_show='AGGTRADES',  # Important: use AGGTRADES for crypto
            output_name='btc_current',
            output_dir='data/crypto'
        )
        
        # Get historical Bitcoin data
        btc_historical = fetcher.get_historical_data(
            symbol='BTC',
            exchange='PAXOS',
            currency='USD',
            duration='1 D',
            bar_size='5 mins',
            what_to_show='AGGTRADES',
            end_datetime='20240101 00:00:00',  # Start of 2024
            output_name='btc_historical',
            output_dir='data/crypto'
        )
        
        return {
            'BTC.USD_current': btc_current,
            'BTC.USD_historical': btc_historical
        }
    finally:
        fetcher.disconnect()

if __name__ == "__main__":
    # Create data directories
    import os
    for dir_name in ['forex', 'crypto']:
        os.makedirs(f'data/{dir_name}', exist_ok=True)
    
    print("Getting forex data...")
    forex_data = get_forex_data()
    for name, df in forex_data.items():
        if df is not None:
            print(f"\n{name} data:")
            print(df.head())
    
    print("\nGetting crypto data...")
    crypto_data = get_crypto_data()
    for name, df in crypto_data.items():
        if df is not None:
            print(f"\n{name} data:")
            print(df.head())
