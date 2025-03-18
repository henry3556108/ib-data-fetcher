# Interactive Brokers Data Fetcher Examples

This directory contains example scripts demonstrating various ways to use the IBDataFetcher class.

## Files

### 1. Basic Examples (`basic_examples.py`)
Simple examples showing how to:
- Get current stock data
- Get historical stock data with specific end dates

### 2. Advanced Examples (`advanced_examples.py`)
More complex examples demonstrating:
- Fetching data for multiple stocks
- Using different market data types (TRADES, BID_ASK, ADJUSTED_LAST)

### 3. Asset Examples (`asset_examples.py`)
Examples for different asset classes:
- Forex data (using IDEALPRO exchange and MIDPOINT data)
- Crypto data (using PAXOS exchange and AGGTRADES data)

## Usage

Each script can be run independently. They all use paper trading port (4002) by default.

```bash
# Run basic examples
python basic_examples.py

# Run advanced examples
python advanced_examples.py

# Run asset-specific examples
python asset_examples.py
```

Data will be saved in the following directories:
- `data/basic/`: Basic example data
- `data/stocks/`: Multiple stock data
- `data/types/`: Different market data types
- `data/forex/`: Forex data
- `data/crypto/`: Crypto data
