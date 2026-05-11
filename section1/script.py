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

BASES = [
    "https://httpstat.us",
    "https://httpbin.org/status",
]
RETRY_LIMIT = 5

# 5 different status codes to request
TARGETS = [200, 201, 301, 404, 500]


def resolve_base() -> str:
    """Try each base URL up to RETRY_LIMIT times; return the first that responds."""
    for i, base in enumerate(BASES):
        fallback = BASES[i + 1] if i + 1 < len(BASES) else None
        if fallback:
            logger.info("Trying %s (will switch to %s after %d failed attempts)", base, fallback, RETRY_LIMIT)
        else:
            logger.info("Trying %s (last available URL)", base)
        for attempt in range(1, RETRY_LIMIT + 1):
            try:
                r = requests.get(f"{base}/200", timeout=5, allow_redirects=False)
                r.raise_for_status()
                logger.info("Using base URL: %s (ok on attempt %d)", base, attempt)
                return base
            except requests.RequestException as exc:
                logger.warning("Attempt %d/%d for %s failed: %s", attempt, RETRY_LIMIT, base, exc)
    raise RuntimeError("All base URLs are unavailable after retries")


def fetch(base: str, status_code: int) -> None:
    url = f"{base}/{status_code}"
    logger.info("GET %s", url)
    response = requests.get(url, timeout=10, allow_redirects=False)
    code = response.status_code

    if code < 400:
        logger.info("OK  status=%d body=%r", code, response.text.strip())
    else:
        raise RuntimeError(f"HTTP error: status={code} body={response.text.strip()!r}")


def main() -> None:
    base = resolve_base()
    for code in TARGETS:
        try:
            fetch(base, code)
        except RuntimeError as exc:
            logger.error("Exception raised: %s", exc)


if __name__ == "__main__":
    main()
