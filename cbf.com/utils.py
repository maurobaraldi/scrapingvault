import csv
import json
import urllib.request
import urllib.error
import ssl
from contextlib import contextmanager
from time import perf_counter

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_json(
    url,
    headers=None,
    verify_ssl=True,
    ignore_status_codes=None,
):
    """
    Fetch and return JSON from a URL.

    Args:
        url (str): The JSON endpoint.
        headers (dict, optional): Additional HTTP headers.
        verify_ssl (bool): Whether to verify SSL certificates.
        ignore_status_codes (Iterable[int], optional):
            HTTP status codes to ignore. If encountered, the status
            code and URL are printed and None is returned.

    Returns:
        dict | list | None
    """
    request_headers = DEFAULT_HEADERS.copy()
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(url, headers=request_headers)

    context = None
    if not verify_ssl:
        context = ssl._create_unverified_context()

    ignored = set(ignore_status_codes or ())

    try:
        with urllib.request.urlopen(request, context=context) as response:
            return json.load(response)

    except urllib.error.HTTPError as e:
        if e.code in ignored:
            print(f"HTTP {e.code}: {url}")
            return None
        
        # Debug purpose
        if e.code == 502:
            import pdb; pdb.set_trace()

        raise RuntimeError(
            f"HTTP Error {e.code}: {e.reason}\n"
            f"{e.read().decode('utf-8', errors='ignore')}"
        ) from e

    except urllib.error.URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}") from e

@contextmanager
def timer(name: str = "Elapsed"):
    start = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(f"{name}: {elapsed:.3f}s")

