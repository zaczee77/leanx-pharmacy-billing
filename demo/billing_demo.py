"""Pharmacy billing worklists, a small reference demo.

This demo shows the worklist pattern behind a pharmacy billing agent:
three guided worklists for routine billing review, rejection follow up,
and eligibility review, plus a session that can be paused, handed off
to another reviewer, and resumed without losing its place.

Every claim, amount, reason code, and reviewer name in this file is
invented sample data written only to exercise the worklist pattern.
Nothing here is a real prescription, a real claim, or a real patient
record. The demo uses plain Python with no external packages and makes
no network calls. No real record ever leaves an approved system in
this demo, because no real record is ever loaded into it.
"""

# Fictional sample claims. Each claim carries the fields one worklist
# needs, and nothing else. Amounts are in dollars.
ROUTINE = [
    {"id": "RX-1001", "amount": 184.20, "missing": []},
    {"id": "RX-1002", "amount": 96.50, "missing": ["days supply"]},
    {"id": "RX-1003", "amount": 212.00, "missing": []},
    {"id": "RX-1004", "amount": 58.75, "missing": ["quantity", "prescriber id"]},
    {"id": "RX-1005", "amount": 143.40, "missing": []},
]

REJECTIONS = [
    {"id": "RX-2001", "amount": 210.30, "reason": "CO-97"},
    {"id": "RX-2002", "amount": 88.10, "reason": "PR-204"},
    {"id": "RX-2003", "amount": 175.60, "reason": "CO-97"},
    {"id": "RX-2004", "amount": 64.25, "reason": "MA-130"},
]

ELIGIBILITY = [
    {"id": "RX-3001", "amount": 132.00, "coverage": "verified"},
    {"id": "RX-3002", "amount": 99.90, "coverage": "pending"},
    {"id": "RX-3003", "amount": 245.80, "coverage": "verified"},
    {"id": "RX-3004", "amount": 71.40, "coverage": "expired"},
]

# Next action for each rejection reason code in the sample data.
REJECTION_ACTIONS = {
    "CO-97": "verify the benefit and resubmit",
    "PR-204": "correct the service date and resubmit",
    "MA-130": "request the missing documentation",
}


def review_routine(claim):
    """Review one routine billing item.

    Returns ready when every required field is present, and flagged
    with the missing fields otherwise.
    """
    if not claim["missing"]:
        return "ready", "all required fields present"
    return "flagged", "missing: " + ", ".join(claim["missing"])


def follow_up_rejection(claim):
    """Route one rejected claim to its next action."""
    action = REJECTION_ACTIONS.get(claim["reason"])
    if action is None:
        return "flagged", "unknown reason code " + claim["reason"]
    return "routed", action


def check_eligibility(claim):
    """Check one eligibility item."""
    if claim["coverage"] == "verified":
        return "covered", "coverage verified"
    if claim["coverage"] == "pending":
        return "waiting", "coverage check still pending"
    return "flagged", "coverage expired, reverify before billing"


class BillingSession:
    """A work session that can pause, hand off, and resume.

    The session owns one worklist at a time and remembers exactly
    where it stopped, so a handoff never redoes finished work and
    never skips an item.
    """

    def __init__(self, owner, items, worker):
        self.owner = owner
        self.items = list(items)
        self.worker = worker
        self.position = 0
        self.results = []
        self.paused = False
        self.events = ["session opened by " + owner]

    def process_next(self):
        """Process the next item, unless the session is paused."""
        if self.paused:
            return None
        if self.position >= len(self.items):
            return None
        item = self.items[self.position]
        outcome, detail = self.worker(item)
        self.results.append((item["id"], outcome, detail))
        self.position += 1
        return item["id"], outcome

    def pause(self):
        """Pause the session, keeping the position as it is."""
        self.paused = True
        self.events.append(
            "paused by %s at item %d of %d"
            % (self.owner, self.position, len(self.items))
        )

    def hand_off(self, new_owner):
        """Hand the session to another reviewer, position unchanged."""
        self.events.append(
            "handed off from %s to %s at item %d of %d"
            % (self.owner, new_owner, self.position, len(self.items))
        )
        self.owner = new_owner

    def resume(self):
        """Resume the session from the exact item where it stopped."""
        self.paused = False
        self.events.append(
            "resumed by %s at item %d of %d"
            % (self.owner, self.position, len(self.items))
        )

    def run_to_end(self):
        """Process every remaining item in this session."""
        while self.process_next() is not None:
            pass
        self.events.append(
            "finished by %s, %d of %d items processed"
            % (self.owner, self.position, len(self.items))
        )


def print_worklist(title, items, worker):
    """Run one worklist from start to finish and print the results."""
    print(title)
    counts = {}
    for item in items:
        outcome, detail = worker(item)
        counts[outcome] = counts.get(outcome, 0) + 1
        print("  %s  $%.2f  %s, %s" % (item["id"], item["amount"], outcome, detail))
    print("  Counts: " + ", ".join(
        "%s %d" % (name, counts[name]) for name in sorted(counts)
    ))
    print()
    return counts


def main():
    print("Pharmacy billing worklists demo")
    print("All claims, amounts, reason codes, and reviewer names are")
    print("invented sample data, written only to exercise the pattern.")
    print()

    print("Worklist 1: routine billing review")
    routine_counts = print_worklist(
        "  Reviewing each claim for the fields billing needs.",
        ROUTINE,
        review_routine,
    )

    print("Worklist 2: rejection follow up")
    rejection_counts = print_worklist(
        "  Routing each rejected claim to its next action.",
        REJECTIONS,
        follow_up_rejection,
    )

    print("Worklist 3: eligibility review")
    eligibility_counts = print_worklist(
        "  Checking coverage before anything is billed.",
        ELIGIBILITY,
        check_eligibility,
    )

    print("Session demo: pause, hand off, resume")
    print("  A session works the routine list again, this time with")
    print("  a pause and a handoff in the middle, to show the place")
    print("  is kept and no item is done twice or skipped.")
    print()
    session = BillingSession("reviewer A", ROUTINE, review_routine)
    session.process_next()
    session.process_next()
    session.pause()
    session.hand_off("reviewer B")
    session.resume()
    session.run_to_end()
    for event in session.events:
        print("  " + event)
    print()
    for claim_id, outcome, detail in session.results:
        print("  %s  %s, %s" % (claim_id, outcome, detail))
    print()

    print("Summary")
    print("  Routine review: %d ready, %d flagged"
          % (routine_counts.get("ready", 0), routine_counts.get("flagged", 0)))
    print("  Rejection follow up: %d routed, %d flagged"
          % (rejection_counts.get("routed", 0), rejection_counts.get("flagged", 0)))
    print("  Eligibility review: %d covered, %d waiting, %d flagged"
          % (eligibility_counts.get("covered", 0),
             eligibility_counts.get("waiting", 0),
             eligibility_counts.get("flagged", 0)))
    print("  Session: %d items processed, pause and handoff kept the"
          % len(session.results))
    print("  place, and every item was handled exactly once.")
    print()
    print("What the demo shows")
    print("  Three small worklists, each with one clear decision per")
    print("  item, and a session that survives a pause and a handoff")
    print("  without losing its place. That is the whole pattern:")
    print("  guided lists, a decision on each item, and work that")
    print("  can stop and start again safely.")


if __name__ == "__main__":
    main()
