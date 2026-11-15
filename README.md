# leanx

leanx is an automated agent for pharmacy billing, built by Nirmeet Rao and presented on his portfolio at nirmeetrao.com. It is live at leanx-nirmeetrao77.replit.app. It works as guided pharmacy billing worklists for routine billing review, rejection follow up, and eligibility review. Work can be paused, handed off, and resumed in session, while prescription and claim records stay in the pharmacy's approved system.

## The problem

Pharmacy billing is a queue that never empties. Every prescription that leaves the counter creates a billing item, and every item needs the same few checks before it can be billed: are the required fields present, was the last attempt rejected and why, and is coverage still valid. The checks are simple on their own, but they pile up across hundreds of items, and the pile is where mistakes happen. A claim billed with a missing field comes back rejected. A rejection nobody follows up on stays unpaid. An eligibility check nobody runs becomes a bill sent to the wrong payer.

The work is also interrupted work. A reviewer starts a list, gets pulled away, and comes back to a list that does not remember where they stopped. Items get done twice, or skipped, or handed to someone else with no record of what is finished. The billing queue needs a shape that survives interruption, not just a shape that works when nobody is interrupted.

## Who it serves

leanx is aimed at pharmacy staff who run billing as part of a working day, not as a separate department. The worklists fit the three jobs that recur every day: the routine review of new billing items, the follow up on rejected claims, and the eligibility check before anything is billed. The session model fits how that work actually happens, in stretches between other duties, handed from one person to another when a shift changes.

## What it does

1. Routine billing review. Each new billing item is checked for the fields billing needs, such as days supply, quantity, and prescriber id. An item with everything present is marked ready. An item with a gap is flagged with the missing fields named, so the fix is obvious.
2. Rejection follow up. Each rejected claim is routed to its next action by its rejection reason, such as verifying the benefit, correcting the service date, or requesting missing documentation. The reason decides the action, so the reviewer does not have to look it up each time.
3. Eligibility review. Coverage is checked before anything is billed. Verified coverage is marked covered, a pending check is marked waiting, and expired coverage is flagged so coverage can be verified again.
4. Pause, hand off, resume. A work session can be paused at any point, handed to another reviewer, and resumed from the exact item where it stopped. Finished items are never redone, and no item is skipped.
5. Records stay put. Prescription and claim records stay in the pharmacy's approved system. The worklists guide the work; they do not move the records.

## Design principles

1. One decision per item. Every item in a worklist ends in a single clear outcome, ready, flagged, routed, covered, or waiting, with the reason attached. A worklist that leaves an item undecided has not done its job.
2. The reason travels with the outcome. A flag without a reason is just a second queue. Every flag in leanx names what is missing or what went wrong, so the next step is visible.
3. Interruption is normal. Work stops and starts again, and people hand work to each other. The session remembers its place, so a pause or a handoff costs nothing and loses nothing.
4. The record stays where it belongs. Billing guidance is useful only if the underlying records stay in the system that owns them. leanx works from the approved system and does not copy records out of it.
5. Nothing is billed on a guess. An item moves forward only when its checks pass. When a check cannot pass, the item waits in the open, flagged and explained, instead of going out and coming back rejected.

## The demo in this repository

The demo folder contains a small reference demo in plain Python with no external packages. It runs three worklists over invented sample claims: routine review finds 3 ready and 2 flagged out of 5 items, rejection follow up routes all 4 rejected claims to a next action, and eligibility review finds 2 covered, 1 waiting, and 1 flagged out of 4 items. It then runs a session over the routine list that processes 2 items, pauses, hands off from reviewer A to reviewer B, resumes at item 2 of 5, and finishes all 5 items with each handled exactly once. The docs folder describes the concept and its design without inventing metrics or outcomes for it.

## What this is not

This demo is not the leanx product. leanx is live at leanx-nirmeetrao77.replit.app, and this repository contains a reference implementation of its worklist pattern only. There are no real prescriptions, no real claims, no real patient records, and no measured results here. The sample claims, amounts, reason codes, and reviewer names are invented and exist only so the pattern can be run and read. Real billing rules, payer specific rejection handling, and live coverage checks are all real parts of pharmacy billing, and none of them are modeled here. The full case study in the docs folder describes the concept and its design without claiming anything beyond what is on the portfolio.

## Links

1. Live product: https://leanx-nirmeetrao77.replit.app
2. Portfolio: https://nirmeetrao.com
3. GitHub: https://github.com/Zaczee77
4. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
