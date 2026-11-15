# leanx case study

## What leanx is

leanx is an automated agent for pharmacy billing, built by Nirmeet Rao and presented on his portfolio at nirmeetrao.com. It is live at leanx-nirmeetrao77.replit.app. This case study describes the problem it addresses, the worklist pattern at its center, and the design choices behind it. It invents no metrics, users, or outcomes for the product, because none are part of its public record.

## The problem in plain terms

Pharmacy billing is a queue that never empties. Every prescription creates a billing item, and every item needs the same few checks before it can be billed: are the required fields present, was the last attempt rejected and why, and is coverage still valid. Each check is simple. The difficulty is volume and interruption. Hundreds of items a day, each needing a decision, worked in stretches between other duties, handed from one person to another when a shift changes.

The failure mode is not a hard check. It is a missed one. A claim billed with a missing field comes back rejected. A rejection nobody follows up on stays unpaid. An eligibility check nobody runs becomes a bill sent to the wrong payer. And a list that does not remember where it stopped creates its own errors: items done twice, items skipped, and a handoff with no record of what is finished.

## The three worklists

leanx organizes the work into three guided worklists, one per recurring job.

Routine billing review covers new items. Each item is checked for the fields billing needs, such as days supply, quantity, and prescriber id. An item with everything present is marked ready. An item with a gap is flagged with the missing fields named, so the fix is visible without opening the record to find it. In the demo that ships with this case study, 3 of 5 routine items are ready and 2 are flagged, each with its missing fields listed.

Rejection follow up covers claims that came back. Each rejected claim is routed to its next action by its rejection reason: verify the benefit, correct the service date, or request missing documentation. The reason decides the action, so the reviewer does not have to look it up each time, and the same reason always gets the same action, which keeps the follow up consistent. In the demo, all 4 rejected claims route to a next action.

Eligibility review covers coverage before anything is billed. Verified coverage is marked covered, a pending check is marked waiting, and expired coverage is flagged so coverage can be verified again. The point is timing: the eligibility question is cheapest to answer before the claim goes out, and most expensive after it comes back. In the demo, 2 of 4 items are covered, 1 is waiting, and 1 is flagged.

## Pause, hand off, resume

The session model is the part of the design that fits how pharmacy work actually happens. A work session can be paused at any point, handed to another reviewer, and resumed from the exact item where it stopped. The session remembers its position, so a pause costs nothing and a handoff loses nothing: finished items are never redone, and no item is skipped.

In the demo, a session works the routine list, processes 2 items, pauses, hands off from reviewer A to reviewer B, resumes at item 2 of 5, and finishes all 5 items with each handled exactly once. That is the whole guarantee, stated small: the work survives interruption. A billing tool that only works when nobody is interrupted does not fit a pharmacy, where interruption is the normal state of the day.

## Records stay in the approved system

Prescription and claim records stay in the pharmacy's approved system. The worklists guide the work; they do not move the records. That boundary matters more in pharmacy than in most billing work, because the records are patient records, and the system that holds them is the one the pharmacy has approved for them. A billing agent that copies records out to work on them would trade a workflow problem for a data problem. leanx keeps the guidance separate from the records, so the work can be organized without the data leaving the place it belongs.

## Design principles

1. One decision per item. Every item in a worklist ends in a single clear outcome, ready, flagged, routed, covered, or waiting, with the reason attached. A worklist that leaves an item undecided has not done its job.
2. The reason travels with the outcome. A flag without a reason is just a second queue. Every flag names what is missing or what went wrong, so the next step is visible.
3. Interruption is normal. Work stops and starts again, and people hand work to each other. The session remembers its place, so a pause or a handoff costs nothing and loses nothing.
4. The record stays where it belongs. Billing guidance is useful only if the underlying records stay in the system that owns them. leanx works from the approved system and does not copy records out of it.
5. Nothing is billed on a guess. An item moves forward only when its checks pass. When a check cannot pass, the item waits in the open, flagged and explained, instead of going out and coming back rejected.

## What the demo shows, and what it does not show

The demo in this repository shows the worklist pattern at miniature scale: three worklists over invented sample claims, one decision per item with the reason attached, and a session that survives a pause and a handoff without losing its place. It shows the shape of the work: guided lists, a decision on each item, and work that can stop and start again safely. It does not show real prescriptions, real claims, real patient records, or measured results, and it does not show the leanx product itself. Real billing rules, payer specific rejection handling, and live coverage checks are all real parts of pharmacy billing, and none of them are modeled in the demo. The demo is a reference implementation of the worklist pattern, written in plain Python with no external packages.

## Links

1. Live product: https://leanx-nirmeetrao77.replit.app
2. Portfolio: https://nirmeetrao.com
3. GitHub: https://github.com/Zaczee77
4. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
