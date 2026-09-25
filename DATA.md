# Data in this repository

Everything under `data/raw/` is real, public data, committed on purpose and **never edited**. Where it came from, its license, and exactly what was changed for this course:

## Frankfurter — ECB euro reference rates, cached

**Source:** the Frankfurter API (https://frankfurter.dev), which serves the European Central Bank's euro foreign
exchange reference rates. Request: `https://api.frankfurter.dev/v1/2016-09-01..2018-10-31?base=EUR&symbols=BRL,USD` (fetched 2026-09-19, SHA-256 `0ad5dd7a88c3c386…`).

**Contract, pinned:** `GET https://api.frankfurter.dev/v1/2016-09-01..2018-10-31?base=EUR&symbols=BRL,USD`.
The response is one JSON object with `amount`, `base` (`"EUR"`), `start_date`, `end_date`, and `rates`, a
dictionary keyed by date whose values are dictionaries keyed by currency. So every number is **units of that
currency per one euro** (e.g. `"BRL": 3.6`). The ECB publishes on its business days only: no weekends, no ECB
holidays.

**License:** ECB statistics may be reused provided the source is acknowledged: *Source: European Central Bank*.
The Frankfurter API is open source (MIT).

**Changes made for this course:** none. The file is the API response exactly as received.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `frankfurter_eur.json` | 22,721 | `0ad5dd7a88c3c386…` |

## Brazilian E-Commerce Public Dataset by Olist — a selected subset

**Source:** Olist, *Brazilian E-Commerce Public Dataset by Olist*, Kaggle,
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce — the original eight CSV files, e.g.
`https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce` (fetched 2026-09-19, SHA-256 `8df58ef3d2d7e994…`).

**License:** **CC BY-NC-SA 4.0**. Attribution: *Brazilian E-Commerce Public Dataset by Olist* (2018).
NonCommercial: this subset is redistributed for non-commercial teaching only. ShareAlike: this subset is an
adaptation and is shared under the same license, CC BY-NC-SA 4.0. The course's own code and text are not
relicensed by it.

**Changes made for this course — this is a SELECTED sample, not a representative one.** 2,653 of the 99,441 orders:
a deterministic 2.5% of orders (by a hash of `order_id`), **plus** every order that contains an item whose
category has no English translation, 40 orders containing items with no category, 25 orders with more than one
review, the orders sharing 15 review ids that span several orders, the one order with no payment row, every order
placed from 1 September 2018 on, and 30 orders from before November 2016. Every child row (items, payments,
reviews) of a selected order is included, and every customer, product, and seller those rows reference, so no
row in this subset refers to a row that is missing. The translation table is complete. No values were edited.
Selected, rather than random, because a random sample of this size can lose the rare situations the labs are
about.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `order_payments.csv` | 151,384 | `a17effc15a7f5bf8…` |
| `orders.csv` | 463,359 | `047d88d8270f9b76…` |

## World Bank — World Development Indicators API, cached pages

**Source:** World Bank Indicators API v2 (https://api.worldbank.org/v2). Requests:
`/country/all/indicator/SP.POP.TOTL?format=json&date=2010:2024&per_page=1000&page=N` (population) and the same
for `NY.GDP.MKTP.PP.KD` (GDP, PPP, constant 2021 international dollars), pages 1 to 4 each; and
`/country?format=json&per_page=400&page=1`, the country metadata. First page: `https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2010:2024&per_page=1000&page=1` (fetched 2026-09-19, SHA-256 `706c1f6ed0f69fb8…`).

**Response shape:** every file is a two-element JSON array. Element 0 is metadata (`page`, `pages`, `per_page`,
`total`). Element 1 is the records. **Each file is one page**: page 1 holds 1,000 of the 3,975 records. The
metadata file's `region` field is `"Aggregates"` for rows that are groups of countries (`WLD`, `EUU`, income
groups), not countries.

**License:** **CC BY 4.0**. Attribution: *World Bank, World Development Indicators*.

**Changes made for this course:** none. Each file is one API response exactly as received.

## Files

| File | Bytes | SHA-256 |
|---|---:|---|
| `SP.POP.TOTL_page1.json` | 210,269 | `706c1f6ed0f69fb8…` |
| `SP.POP.TOTL_page2.json` | 197,327 | `649de57d4a1ebad7…` |
| `SP.POP.TOTL_page3.json` | 197,141 | `4039e5bf43ba298e…` |
| `SP.POP.TOTL_page4.json` | 194,617 | `542c48f24a13b6c2…` |
| `country_page1.json` | 113,590 | `d29d57f8adf954c5…` |

## Lecture toy — three real rates, `api/toy_rates.json`

**What it is:** a three-entry document for the Block 4 lecture, cut by hand from `api/frankfurter_eur.json` above.
It keeps that response's `amount` (`1.0`) and `base` (`"EUR"`), and three dates, 2017-01-02, 2017-01-03 and
2017-01-04, each with its `BRL` value only. Every other date, the `USD` values, `start_date` and `end_date` were
removed. **No value was changed:** each number is the ECB's reais per one euro on that day, exactly as the cached
response has it. The file is pretty-printed so it can be read in VS Code; the cached response is not.

**Source and license:** as for the Frankfurter cache above — *Source: European Central Bank*, via Frankfurter.
