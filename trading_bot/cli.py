import argparse
import logging
from binance.error import ClientError, ServerError
from bot.validators import validate
from bot.orders import place_order
from bot.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet order bot")
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--qty", required=True, type=float)
    parser.add_argument("--price", type=float)
    return parser.parse_args()


def main():
    args = parse_args()

    # --- Input validation ---
    try:
        validate(args)
    except ValueError as e:
        logger.error("Invalid input: %s", e)
        raise SystemExit(f"Error: {e}")

    msg = f"Placing {args.side} {args.type} order: {args.qty} {args.symbol}"
    if args.price is not None:
        msg += f" @ {args.price}"
    logger.info(msg)

    # --- API call with structured error handling ---
    try:
        response = place_order(args.symbol, args.side, args.type, args.qty, args.price)

    except ClientError as e:
        logger.error("Binance rejected the order: [%s] %s", e.error_code, e.error_message)
        raise SystemExit(f"Order rejected: {e.error_message}")

    except ServerError as e:
        logger.error("Binance server error (status %s) — try again later", e.status_code)
        raise SystemExit("Binance server error. Try again later.")

    except Exception as e:
        logger.error("Unexpected error: %s: %s", type(e).__name__, e)
        raise SystemExit(f"Unexpected error: {e}")

    # --- Success output ---
    logger.info(
        "Order filled | id=%s status=%s executedQty=%s avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice"),
    )
    print("ORDER ID   :", response.get("orderId"))
    print("Status     :", response.get("status"))
    print("ExecutedQty:", response.get("executedQty"))
    print("Price      :", response.get("avgPrice"))


if __name__ == "__main__":
    main()
