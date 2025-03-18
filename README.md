# Interactive Brokers Historical Data Fetcher

A Python tool for fetching historical market data from Interactive Brokers using the `ib_insync` library.

## Prerequisites

- Interactive Brokers Account
- IB Gateway or TWS (Trader Workstation) installed and running
- Python 3.8 or higher

## Installation

1. Create a conda environment and install dependencies:
```bash
conda create -n stockdata python=3.8
conda activate stockdata
pip install -r requirements.txt
```

## Configuration

Before using the tool, make sure:
1. IB Gateway/TWS is running
2. API connections are enabled in TWS/Gateway settings
3. Use the correct port for your setup:
   - TWS Live: 7496 (Real trading in TWS)
   - TWS Paper: 7497 (Paper trading in TWS)
   - IB Gateway Live: 4001 (Real trading in Gateway)
   - IB Gateway Paper: 4002 (Paper trading in Gateway)

**Important**: Always start with paper trading (ports 7497 or 4002) for testing!

## Data Parameters

### Duration Units
| Unit | Description |
|------|-------------|
| S | Seconds |
| D | Day |
| W | Week |
| M | Month |
| Y | Year |

Example format: '1 Y', '6 M', '10 D'

### Bar Sizes
| Category | Available Sizes |
|----------|----------------|
| Seconds | 1, 5, 10, 15, 30 secs |
| Minutes | 1, 2, 3, 5, 10, 15, 20, 30 mins |
| Hours | 1, 2, 3, 4, 8 hours |
| Days+ | 1 day, 1 week, 1 month |

### Data Types
- `TRADES`: Default. Adjusted for splits but not dividends
- `BID`: Bid prices
- `ASK`: Ask prices
- `MIDPOINT`: Midpoint between bid/ask (recommended for forex)
- `BID_ASK`: Both bid and ask prices
- `ADJUSTED_LAST`: Adjusted for both splits and dividends (TWS 967+ only)
- `SCHEDULE`: Trading schedule, only available with 1-day bars (TWS API 10.12+ only)
- `AGGTRADES`: Only available for crypto contracts

## Usage

### Basic Usage

```python
from test import IBDataFetcher

# Create instance (use port 4001 for live trading, 4002 for paper)
fetcher = IBDataFetcher(port=4001)

try:
    # Get current data
    df = fetcher.get_historical_data(
        symbol='SPY',
        duration='1 Y',
        bar_size='1 hour',
        output_name='spy_data',
        output_dir='data'
    )
    
    # Get historical data for specific date
    df_historical = fetcher.get_historical_data(
        symbol='SPY',
        duration='1 Y',
        bar_size='1 hour',
        end_datetime='20231231 16:00:00',  # End at market close
        output_name='spy_2023_data',
        output_dir='data'
    )
finally:
    fetcher.disconnect()
```

### Examples

#### Get current 5-minute bars
```python
df = fetcher.get_historical_data(
    symbol='AAPL',
    duration='1 D',
    bar_size='5 mins',
    what_to_show='TRADES'
)
```

#### Get historical daily data for 2023
```python
df = fetcher.get_historical_data(
    symbol='TSLA',
    duration='1 Y',
    bar_size='1 day',
    what_to_show='ADJUSTED_LAST',  # Includes dividend adjustments
    end_datetime='20231231 23:59:59'  # End at year end
)
```

#### Get forex data for specific week
```python
df = fetcher.get_historical_data(
    symbol='EUR',
    exchange='IDEALPRO',  # Use IDEALPRO for forex
    currency='USD',
    duration='1 W',
    bar_size='1 hour',
    what_to_show='MIDPOINT',  # Recommended for forex
    end_datetime='20240101 00:00:00'  # First week of 2024
)
```

## Output Format

The data is returned as a pandas DataFrame with the following columns:
- date: Timestamp of the bar
- open: Opening price
- high: Highest price
- low: Lowest price
- close: Closing price
- volume: Trading volume
- average: Volume Weighted Average Price (VWAP)
- barCount: Number of trades in this bar

## Error Handling

The tool includes comprehensive error handling for:
- Invalid parameters (duration, bar size, data type)
- Connection issues
- Data retrieval failures
- Parameter combination restrictions

## Best Practices

1. Always disconnect after use using `fetcher.disconnect()`
2. Use try-finally blocks to ensure proper cleanup
3. Start with smaller time periods for testing
4. Use appropriate bar sizes for your timeframe:
   - Seconds/minutes for intraday analysis
   - Hours/days for longer-term analysis
5. Consider using Regular Trading Hours (use_rth=True) for more reliable data
6. For forex, use `MIDPOINT` data type and `IDEALPRO` exchange
7. For stocks with dividends, use `ADJUSTED_LAST` to get dividend-adjusted prices
8. When requesting historical data:
   - Use market hours for end_datetime (e.g., 16:00:00 for US stocks)
   - Consider timezone differences
   - Format dates as 'YYYYMMDD HH:mm:ss'

## License

This project is licensed under the MIT License.