import time
import logging
from .client import client, safe_request

logger = logging.getLogger(__name__)


def place_order(symbol, side, order_type, qty, price=None):
    params = dict(symbol=symbol, side=side, type=order_type, quantity=qty)
    if price is not None:
        params["price"] = price
        params["timeInForce"] = "GTC"

    response = safe_request(client.new_order, **params)
    time.sleep(1)
    return safe_request(client.query_order, symbol=symbol, orderId=response["orderId"])
