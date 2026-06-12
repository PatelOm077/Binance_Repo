A Python bot for placing MARKET and LIMIT orders on Binance USDT-M Futures Testnet. Comes with a CLI and a small web UI.

---
Setup

1. Install dependencies:
pip install -r requirements.txt
2. Create a .env file inside the trading_bot/ folder:
BINANCE_API_KEY=your_api_key_here
BINANCE_AUTH_KEY=your_secret_key_here
2. Get your keys from https://testnet.binancefuture.com â API Management.

---
CLI Usage

Run from inside the trading_bot/ directory.

# Market buy
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

# Market sell
python cli.py --symbol ETHUSDT --side SELL --type MARKET --qty 0.01

# Limit buy
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 50000

# Limit sell
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 70000

Arguments:

ââââââââââââ¬ââââââââââââââââ¬ââââââââââââââââââââââââââââââââââââââââââââ
â   Flag   â   Required    â                Description                â
ââââââââââââ¼ââââââââââââââââ¼ââââââââââââââââââââââââââââââââââââââââââââ¤
â --symbol â Yes           â Trading pair (e.g. BTCUSDT, ETHUSDT,      â
â          â               â BNBUSDT)                                  â
ââââââââââââ¼ââââââââââââââââ¼ââââââââââââââââââââââââââââââââââââââââââââ¤
â --side   â Yes           â BUY or SELL                               â
ââââââââââââ¼ââââââââââââââââ¼ââââââââââââââââââââââââââââââââââââââââââââ¤
â --type   â Yes           â MARKET or LIMIT                           â
ââââââââââââ¼ââââââââââââââââ¼ââââââââââââââââââââââââââââââââââââââââââââ¤
â --qty    â Yes           â Order quantity                            â
ââââââââââââ¼ââââââââââââââââ¼ââââââââââââââââââââââââââââââââââââââââââââ¤
â --price  â Only for      â Limit price in USDT                       â
â          â LIMIT         â                                           â
ââââââââââââ´ââââââââââââââââ´ââââââââââââââââââââââââââââââââââââââââââââ

---
Web UI (Bonus)

cd trading_bot
uvicorn app:app --reload

Open http://localhost:8000 in your browser. Fill in the form, hit Place Order, and the result shows up on the same page.

---
Project Structure

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

---
Assumptions

- Supported symbols: BTCUSDT, ETHUSDT, BNBUSDT (add more in validators.py)
- LIMIT orders use timeInForce=GTC (Good Till Cancelled)
- All orders go to the Testnet â no real funds involved
- Logs are written to bot.log in the trading_bot/ directory (both file and console)

---
Logs

All requests, responses, and errors are logged to bot.log. Sample log entries from a MARKET and LIMIT order are included in the repo root.
