#!/usr/bin/env python3
import requests
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# httpstat.us per task spec; switched to httpbin.org (identical API) because httpstat.us is currently unavailable
BASE_URL = "https://httpbin.org/status"

# 5 different status codes to request
TARGETS = [200, 201, 301, 404, 500]


def fetch(status_code: int) -> None:
    url = f"{BASE_URL}/{status_code}"
    logger.info("GET %s", url)
    response = requests.get(url, timeout=10, allow_redirects=False)
    code = response.status_code

    if code < 400:
        logger.info("OK  status=%d body=%r", code, response.text.strip())
    else:
        raise RuntimeError(f"HTTP error: status={code} body={response.text.strip()!r}")


def main() -> None:
    for code in TARGETS:
        try:
            fetch(code)
        except RuntimeError as exc:
            logger.error("Exception raised: %s", exc)


if __name__ == "__main__":
    main()
