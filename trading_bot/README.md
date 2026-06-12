# Binance Futures Testnet Trading Bot

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `trading_bot/` directory:

```
BINANCE_API_KEY=your_api_key
BINANCE_AUTH_KEY=your_secret_key
```

## Usage

Run from inside the `trading_bot/` directory:

```bash
# Market order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

# Limit order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 30000
```
