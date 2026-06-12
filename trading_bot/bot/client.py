import logging
import os
from binance.um_futures import UMFutures
from binance.error import ClientError, ServerError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_api_key = os.getenv("BINANCE_API_KEY")
_secret = os.getenv("BINANCE_AUTH_KEY")

if not _api_key or not _secret:
    raise EnvironmentError(
        "BINANCE_API_KEY and BINANCE_AUTH_KEY must be set in your .env file"
    )

client = UMFutures(
    key=_api_key,
    secret=_secret,
    base_url="https://testnet.binancefuture.com",
)


def safe_request(func, *args, **kwargs):
    # What is this function?
    # Binance has its own functions like client.new_order() or client.query_order().
    # Instead of calling those directly everywhere, we call safe_request() and
    # pass the function we want to run — it adds logging around it automatically.

    # func.__name__ just gives us the name of the function as a string (e.g. "new_order")
    # so our log messages say which Binance call was made.
    function_name = func.__name__

    logger.info("Calling Binance: %s | with inputs: args=%s kwargs=%s", function_name, args, kwargs)

    try:
        # Call the actual Binance function (e.g. client.new_order) with whatever
        # arguments were passed in. This is the line that talks to Binance.
        response = func(*args, **kwargs)

        logger.info("Binance responded OK: %s | response: %s", function_name, response)
        return response

    except ClientError as e:
        # ClientError = YOUR fault (bad symbol, wrong price, not enough balance, etc.)
        # Binance understood the request but rejected it.
        logger.error(
            "Binance rejected the request: %s | http=%s code=%s reason=%s",
            function_name, e.status_code, e.error_code, e.error_message,
        )
        raise  # pass the error up so the route in app.py can show it to the user

    except ServerError as e:
        # ServerError = BINANCE's fault (their servers are down or broken)
        logger.error("Binance server error: %s | http status=%s", function_name, e.status_code)
        raise

    except Exception as e:
        # Anything else — no internet, DNS failure, timeout, etc.
        logger.error("Network/unknown error: %s | %s: %s", function_name, type(e).__name__, e)
        raise
