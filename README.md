# Lab 4 — The revenue that was converted the wrong way

**ECBS5294 — Working with Data · Session 2, Block 4**

## Start here

| | |
|---|---|
| **The question** | What was Olist's revenue in euros, month by month? |
| **The files** | `data/raw/orders.csv`, `data/raw/order_payments.csv`, and the exchange rates, `data/raw/api/frankfurter_eur.json` (a saved answer from an API). |
| **What is wrong** | The report runs without an error, and its euro total is larger than its reais total. |
| **What you hand in** | `DIAGNOSIS.md` on Moodle, before you leave. |
| **First thing to do** | Check that the clone and `uv sync` you started during the stretch finished; then run the notebook top to bottom and read the numbers the report prints. |

## Get the project

If you cloned it during the stretch, you already have it. Otherwise, in your terminal (Git Bash on Windows,
Terminal on macOS), in the folder where you keep course work:

```bash
git clone https://github.com/earino/ecbs5294-lab04-json-api.git
cd ecbs5294-lab04-json-api
uv sync
```

Open **this folder** in VS Code (*File → Open Folder…*; trust the authors if asked), open `notebooks/report.ipynb`,
pick the `.venv` kernel, and run all cells. The first code cell prints the folder it is working in: it must be this
project's folder.

`notebooks/lecture.ipynb` is the lecture's complete demo notebook — every query Eduardo ran on the projector, for
review after class — and it reads the files in `data/raw/api/worldbank/` and `data/raw/api/toy_rates.json`. This lab
is about `report.ipynb` and the Frankfurter file.

## What is broken

The report says Olist's customers paid **435,300.95 reais**, and that this is **1,303,825.60 euros**.

On every day from 2016 to 2018, one Brazilian real was worth less than one euro. You can check that in any published
history of the exchange rate. So the euros should be fewer than the reais, not three times as many.

Nothing errors. Find out why, before you change anything.

**A second problem, disclosed so you do not spend the lab on it.** The report's table by weekday has **five rows**. The
reason: the ECB publishes rates on its business days only — no weekends, no ECB holidays — and **625 of the 2,652
paid orders** were placed on such a day, so the report's join on the exact date finds no rate for them and drops
them. You do not need to diagnose this; section A shows you the count. You do need to **handle** it: your monthly
query must keep those orders, and your check must count any order that ends up with no euro value.

## What you must produce

Work in the notebook, under **Your work starts here**, top to bottom:

1. **Read the document** (section A). Run the two supplied cells: what does the JSON say about its own numbers? Then
   the supplied three counts for the report's join to the rates, which show the disclosed problem. Paste what you
   found into `DIAGNOSIS.md`, part 3, **before you change anything**.
2. **The rates table, the right way round** (section B). From the empty cell: a Python loop that builds `eur_rates`,
   one row per date per currency, with the euros one unit of that currency buys. Take the direction from the
   document's own fields.
3. **Prove the direction** (section C). One order, converted by hand from the JSON's number, and by your table. They
   must agree **to the cent**. **This is the evidence the lab requires**, not the total: a total can look right and
   be wrong.
4. **Monthly revenue in euros** (section D). From the empty cell, to the finance team's definition: each order at the
   average of the month's daily rates. Every order in exactly once, including the 625.
5. **The check** (section E): the count of orders with no euro value, which must be 0 (this is the check for the
   disclosed problem); the order count; the reais, which must add up to `order_revenue`'s total to the cent; and the
   range bound, labelled as what it is — a plausibility check, not a proof.
6. **The corrected total** (section F), and the supplied cell that keeps your table in `data/silver/`.
7. `DIAGNOSIS.md`, all five parts, short. **Keep at least five minutes for it**: start by minute 22 at the latest,
   finished or not. Then the last ten minutes, below, and the Moodle checkpoint.

**Money is compared to the cent, never with `==`.** Two ways of adding up the same money can differ in the last
digit of a float while the cents agree. Write `abs(a - b) < 0.005`, or round both to two decimals first. Counts of
orders are whole numbers: those may use `==`.

## Rules

- **Never edit `data/raw/`.** The saved API answer is the evidence. Fix the code.
- A total that looks right is not the fix. A small edit to the report can make its total plausible and leave the
  table as ambiguous as it was. The required evidence is the table that says which way its rate goes, and the hand
  calculation that proves it.
- `scripts/fetch.py` shows how the file was fetched. You never need to run it; it never overwrites the file.
- You may use AI to explain an error or a function. You must be able to explain every line you hand in: your
  neighbour will ask, at minute 33, without notes.

## Hints, if stuck

Staff will say these over the room at minutes 5, 10, and 15. Read them earlier if you want.

1. Read the document's own fields before its numbers. Section A's first cell prints everything except the rates.
   Which field tells you what the numbers are measured *per*?
2. Take one order on one weekday. Write down its reais, that day's `BRL` number from the JSON, and the report's
   euros for it. Which arithmetic turns the first two into a sensible third?
3. `base` is `EUR` and `amount` is `1.0`: each number is **reais for one euro**. So how many euros is one real? That
   is the number your table's `eur_per_unit` should hold for `BRL`.

## Diagnosis note

In `DIAGNOSIS.md`: the template is there, and you write it in class, in the last five minutes before minute 33.
Parts 1 and 2 are about the direction problem; add one line on the disclosed one. Part 3 is section A's output,
pasted. Part 4 is your loop and your monthly query. Part 5 is section C's two numbers and section E's check, pasted,
with the identity each one tests. (On the single-table route, the section below says what changes.)

## Stretch task

(a) The same revenue in US dollars, from the second currency in your table; and the identity that ties the two
currencies together, checked on three dates. (b) Daily conversion, with the last available rate for days that have
none, using DuckDB's `ASOF JOIN`; compare its euro total with section D's and say which definition your note should
carry. (c) **Write one request yourself**: ask Frankfurter for one day, with its parameters, a timeout and a named
`User-Agent`; check the status; save the answer under `output/` and compare it with that day in the cache. It needs
the network, so it sits behind a `LIVE = False` switch; the lab itself never does. All three are described at the
end of the notebook.

## If the instructor announces it: the single-table route

**Only if the instructor says so at the start of the lab.** If it is not announced, ignore this section and R1 to R4
at the end of the notebook. If it is, this is your whole route; the rules, the hints and the last ten minutes do not
change.

1. **Sections A, B and C**, as above. The rates table and the hand calculation are still the lab.
2. **R1, R2, R3**, at the end of the notebook, **instead of section D**: three questions, each one query from an empty
   cell on one table (`GROUP BY`, `HAVING`, a NULL-safe filter). Write how many rows you expect, and why, before you
   run each one.
3. **R4, instead of section E**: two checks on your `eur_rates`, asserted and printed. Its grain: no date and
   currency pair twice, and rows = days × currencies. Its direction, as plausibility: every `BRL` row's
   `eur_per_unit` is below 1.
4. **Section F's last cell** (supplied), which keeps your table in `data/silver/`. Skip F's corrected total and the
   stretch. The monthly query, its check and the corrected total move to Homework 2, whose first repair is that query.
5. **`DIAGNOSIS.md`**, all five parts, by minute 22 at the latest:
   - Parts 1 and 2: the direction problem, as for everyone. In part 2, one line on the disclosed one: 625 orders have
     no rate on their own day, and the monthly query that keeps them is Homework 2's.
   - Part 3: section A's output, pasted.
   - Part 4: your loop, and your three queries, each with what it returned.
   - Part 5: section C's two numbers and R4's printed line, pasted, with what each one tests.

## Git thread

`data/raw/api/` is committed on purpose: it is the evidence, with its source in `DATA.md`. Your `eur_rates` table is
made by the notebook, so its CSV goes to `data/silver/`, which Git ignores: run `git status` after section F and see
that it is not listed. Commit after your table and your proof work, and again after section D (on the
single-table route, after R4). A commit that changes
a join carries **the three counts** in its message: "Monthly EUR at the month's average rate: 2,652 orders in, 2,652
rows out, 2,652 distinct" — not "fix".

## The last ten minutes

At minute 33, finished or not, turn to the person next to you (three if the row is odd). One of you explains, about a
minute: what was wrong, why, the query that proved it, what you changed, how you know it is right. Point at the
screen; do not read the note. The other asks:

1. **Show me the query that proves it.**
2. **Why was it wrong, not just where?**
3. **The what-if question on the slide.**

Then swap. If either of you is unsure, or you disagree, put a hand up: staff come to you first. Then the answer to
the what-if, for everyone. An unfinished repair is explained the same way: what you found so far.

Before you leave: the lab's **checkpoint on Moodle**. Upload `DIAGNOSIS.md` with its first line filled in. That is
what "complete" means; nobody signs you off.

## If you got lost: how to reset

Both of these **destroy work**. Read before running.

**Discard uncommitted changes (destructive)** — throw away edits and new files; keep your commits:

```bash
git restore --staged --worktree .    # every tracked file back to the last commit, staged or not
git clean -fd                        # and remove new, untracked files
```

> ⚠️ Permanently deletes uncommitted changes, staged or not, and any new untracked files.

**Full reset to the starter state (destructive)** — back to exactly what you cloned; throws away your commits too:

```bash
git reset --hard origin/main
git clean -fdx
```

> ⚠️ Discards your local commits and uncommitted changes. The `-x` also removes ignored files — `data/silver/`, the
> `.venv/` environment — so the folder matches a fresh clone. `uv sync` rebuilds the environment in a minute.
