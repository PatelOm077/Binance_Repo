# Binance Futures Testnet Trading Bot

A Python bot for placing MARKET and LIMIT orders on Binance USDT-M Futures Testnet. Comes with a CLI and a small web UI.

---

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file inside the `trading_bot/` folder:
   ```
   BINANCE_API_KEY=your_api_key_here
   BINANCE_AUTH_KEY=your_secret_key_here
   ```
   Get your keys from [testnet.binancefuture.com](https://testnet.binancefuture.com) → API Management.

---

## CLI Usage

Run from inside the `trading_bot/` directory.

```bash
# Market buy
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

# Market sell
python cli.py --symbol ETHUSDT --side SELL --type MARKET --qty 0.01

# Limit buy
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 50000

# Limit sell
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 70000
```

**Arguments:**

| Flag | Required | Description |
|------|----------|-------------|
| `--symbol` | Yes | Trading pair (e.g. BTCUSDT, ETHUSDT, BNBUSDT) |
| `--side` | Yes | BUY or SELL |
| `--type` | Yes | MARKET or LIMIT |
| `--qty` | Yes | Order quantity |
| `--price` | Only for LIMIT | Limit price in USDT |

---

## Web UI (Bonus)

```bash
cd trading_bot
uvicorn app:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser. Fill in the form, hit Place Order, and the result shows up on the same page.

---

## Project Structure

```
trading_bot/
  bot/
    client.py          # Binance client + safe_request wrapper
    orders.py          # order placement + query logic
    validators.py      # input validation
    logging_config.py  # logging setup (file + console)
  cli.py               # CLI entry point
  app.py               # Web UI (FastAPI)
  templates/
    index.html         # order form + result display
  requirements.txt
```

---

## Assumptions

- Supported symbols: BTCUSDT, ETHUSDT, BNBUSDT (add more in `validators.py`)
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled)
- All orders go to the Testnet — no real funds involved
- Logs are written to `bot.log` in the `trading_bot/` directory (both file and console)

---

## Logs

All requests, responses, and errors are logged to `bot.log`. Sample log entries from a MARKET and LIMIT order are included in the repo root.
