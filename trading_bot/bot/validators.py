VALID_SYMBOLS = {"BTCUSDT", "ETHUSDT", "BNBUSDT"}  # extend as needed


def validate(args):
    if args.symbol not in VALID_SYMBOLS:
        raise ValueError(
            f"Unknown symbol '{args.symbol}'. Valid: {', '.join(sorted(VALID_SYMBOLS))}"
        )
    if args.type == "LIMIT" and args.price is None:
        raise ValueError("--price is required for a LIMIT order")
    if args.qty <= 0:
        raise ValueError("--qty must be greater than 0")
    if args.type == "LIMIT" and args.price <= 0:
        raise ValueError("--price must be greater than 0")
