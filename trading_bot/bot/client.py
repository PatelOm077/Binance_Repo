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
    function_name = func.__name__
    logger.info("Calling Binance: %s | args=%s kwargs=%s", function_name, args, kwargs)

    try:
        # Call the actual Binance function (e.g. client.new_order) with whatever
        # arguments were passed in. This is the line that talks to Binance.
        response = func(*args, **kwargs)

        logger.info("Binance responded OK: %s | response: %s", function_name, response)
        return response

    except ClientError as e:
        logger.error(
            "Binance rejected: %s | http=%s code=%s reason=%s",
            function_name, e.status_code, e.error_code, e.error_message,
        )
        raise

    except ServerError as e:
        logger.error("Binance server error: %s | http=%s", function_name, e.status_code)
        raise

    except Exception as e:
        logger.error("Unexpected error: %s | %s: %s", function_name, type(e).__name__, e)
        raise
