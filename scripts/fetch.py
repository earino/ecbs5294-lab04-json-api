"""Where data/raw/api/frankfurter_eur.json came from, as code. You never need to run this for the lab.

    uv run python scripts/fetch.py           # no network: print the request and check the cached file
    uv run python scripts/fetch.py --live    # one request to the API; compare its answer with the cache

The cache is the lab's data and it is never overwritten. With --live, the fresh answer is written to
output/frankfurter_eur_live.json (Git ignores output/), and the script says whether it matches the cache byte for byte.
It uses only Python's standard library, so it needs nothing installed.
"""
from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

# The pinned request. The caller chooses the base and the symbols; the response repeats the base back.
URL = "https://api.frankfurter.dev/v1/2016-09-01..2018-10-31?base=EUR&symbols=BRL,USD"
CACHE = Path("data/raw/api/frankfurter_eur.json")
LIVE = Path("output/frankfurter_eur_live.json")
HEADERS = {"User-Agent": "ecbs5294-lab04 (course exercise)"}   # say who is asking; this API refuses anonymous scripts


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def describe(data: bytes, label: str) -> None:
    doc = json.loads(data)
    days = sorted(doc["rates"])
    currencies = sorted({c for values in doc["rates"].values() for c in values})
    print(f"{label}: base {doc['base']}, amount {doc['amount']}, {len(days)} days from {days[0]} to {days[-1]}, "
          f"currencies {currencies}, SHA-256 {sha256(data)[:16]}")


def main(argv: list[str]) -> int:
    if not CACHE.exists():
        print(f"Run this from the project folder: {CACHE} not found from {Path.cwd()}")
        return 1
    print("request:", URL)
    cached = CACHE.read_bytes()
    describe(cached, "cache")
    if "--live" not in argv:
        print("(no request made; add --live to ask the API once)")
        return 0
    request = urllib.request.Request(URL, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:   # never wait forever
        print("status:", response.status)
        live = response.read()
    LIVE.parent.mkdir(exist_ok=True)
    LIVE.write_bytes(live)
    describe(live, "live ")
    print("the live answer matches the cache byte for byte" if live == cached
          else f"the live answer differs from the cache; it is in {LIVE} — compare them before you trust either")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
