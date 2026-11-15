# Demo: pharmacy billing worklists

A small reference demo of the worklist pattern behind leanx. It runs three guided worklists over invented sample claims, then shows a session that can be paused, handed off to another reviewer, and resumed without losing its place.

## How to run it

From the repository root, or from this folder:

```
python3 demo/billing_demo.py
```

Plain Python, no external packages, no network calls.

## What it does

1. Routine billing review. Checks 5 invented claims for the fields billing needs. A claim with everything present is marked ready, a claim with a gap is flagged with the missing fields named.
2. Rejection follow up. Routes 4 invented rejected claims to a next action by their rejection reason code.
3. Eligibility review. Checks coverage on 4 invented items: covered, waiting on a pending check, or flagged for expired coverage.
4. Session demo. Runs the routine list a second time inside a session that processes 2 items, pauses, hands off from reviewer A to reviewer B, resumes at item 2 of 5, and finishes all 5 items with each handled exactly once.

## What it printed when it was tested

Routine review: 3 ready, 2 flagged. Rejection follow up: 4 routed, 0 flagged. Eligibility review: 2 covered, 1 waiting, 1 flagged. Session: paused at item 2 of 5, handed off from reviewer A to reviewer B, resumed at item 2 of 5, finished 5 of 5 items, every item handled exactly once.

## What the sample data is

Every claim, amount, reason code, and reviewer name in `billing_demo.py` is invented sample data written only to exercise the worklist pattern. Nothing here is a real prescription, a real claim, or a real patient record. No real record is ever loaded, and no real billing rule is modeled. The demo shows the shape of the work, not the leanx product itself.

## Files

1. `billing_demo.py`: the demo. Worklist functions, the session class, and the printed run.
2. `README.md`: this file.
