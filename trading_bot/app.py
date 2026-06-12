import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from binance.error import ClientError, ServerError
from bot.validators import validate as validate_order
from bot.orders import place_order
from bot.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class _Args:
    """Thin wrapper so validators work with form data the same way as argparse."""
    def __init__(self, symbol, side, order_type, qty, price):
        self.symbol = symbol
        self.side = side
        self.type = order_type
        self.qty = qty
        self.price = price


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/order", response_class=HTMLResponse)
async def submit_order(
    request: Request,
    symbol: str = Form(...),
    side: str = Form(...),
    type: str = Form(...),
    qty: str = Form(...),
    price: str = Form(""),
):
    symbol = symbol.strip().upper()
    price_raw = price.strip()

    try:
        qty_val = float(qty)
    except ValueError:
        return templates.TemplateResponse(
            request, "index.html", {"error": "Quantity must be a number."}
        )

    price_val = None
    if price_raw:
        try:
            price_val = float(price_raw)
        except ValueError:
            return templates.TemplateResponse(
                request, "index.html", {"error": "Price must be a number."}
            )

    args = _Args(symbol, side, type, qty_val, price_val)

    try:
        validate_order(args)
    except ValueError as e:
        return templates.TemplateResponse(
            request, "index.html", {"error": str(e)}
        )

    try:
        response = place_order(symbol, side, type, qty_val, price_val)
    except ClientError as e:
        logger.error("ClientError: [%s] %s", e.error_code, e.error_message)
        return templates.TemplateResponse(
            request, "index.html", {"error": f"Binance rejected: {e.error_message}"}
        )
    except ServerError as e:
        logger.error("ServerError: status=%s", e.status_code)
        return templates.TemplateResponse(
            request, "index.html", {"error": "Binance server error. Try again later."}
        )
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return templates.TemplateResponse(
            request, "index.html", {"error": f"Unexpected error: {e}"}
        )

    result = {
        "order_id":     response.get("orderId"),
        "status":       response.get("status"),
        "executed_qty": response.get("executedQty"),
        "avg_price":    response.get("avgPrice"),
        "symbol":       symbol,
        "side":         side,
        "type":         type,
    }
    return templates.TemplateResponse(request, "index.html", {"result": result})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
