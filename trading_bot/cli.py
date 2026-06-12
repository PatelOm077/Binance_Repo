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

    summary = f"{args.side} {args.type} {args.qty} {args.symbol}"
    if args.price is not None:
        summary += f" @ {args.price}"
    print(f"\nPlacing order: {summary}")
    logger.info("Placing order: %s", summary)

    try:
        response = place_order(args.symbol, args.side, args.type, args.qty, args.price)

    except ClientError as e:
        logger.error("Binance rejected the order: [%s] %s", e.error_code, e.error_message)
        print(f"\nFailed: {e.error_message}")
        raise SystemExit(1)

    except ServerError as e:
        logger.error("Binance server error (status %s) — try again later", e.status_code)
        print("\nFailed: Binance server error. Try again later.")
        raise SystemExit(1)

    except Exception as e:
        logger.error("Unexpected error: %s: %s", type(e).__name__, e)
        print(f"\nFailed: {e}")
        raise SystemExit(1)

    logger.info(
        "Order placed | id=%s status=%s executedQty=%s avgPrice=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
        response.get("avgPrice"),
    )
    print("\nOrder placed successfully!")
    print(f"  Order ID    : {response.get('orderId')}")
    print(f"  Status      : {response.get('status')}")
    print(f"  Executed Qty: {response.get('executedQty')}")
    print(f"  Avg Price   : {response.get('avgPrice')}")


if __name__ == "__main__":
    main()
