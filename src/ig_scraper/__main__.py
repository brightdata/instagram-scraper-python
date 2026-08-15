"""ig-scraper nasa natgeo, or python -m ig_scraper nasa natgeo"""

from __future__ import annotations

import argparse
import sys

from brightdata import BrightDataError
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from .scrape import client_context, scrape_handle, write

#: A spinner and a running clock, so a minute of waiting looks alive.
WAITING = (SpinnerColumn(), TextColumn("{task.description}"), TimeElapsedColumn())


def positive(value: str) -> int:
    """Reject a limit the API would charge for and not honour."""
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError(f"{value} is not 1 or more")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ig-scraper",
        description="Scrape recent Instagram posts for one or more handles.",
    )
    parser.add_argument("handles", nargs="+", help="handles, with or without the @")
    parser.add_argument("--limit", type=positive, default=5, help="posts per handle, default 5")
    parser.add_argument("--out", default="instagram.json", help="output file")
    args = parser.parse_args(argv)

    print(
        f"Fetching up to {args.limit} recent posts per account, for: {', '.join(args.handles)}\n"
        "Usually one to three minutes each. One credit per post, 5,000 free per month."
    )

    outcomes = []
    try:
        with client_context() as client, Progress(*WAITING, transient=True) as bar:
            for handle in args.handles:
                if not bar.console.is_terminal:
                    print(f"asking  @{handle}...", flush=True)  # a log wants a line, not a spinner
                task = bar.add_task(f"@{handle}")
                outcome = scrape_handle(client, handle, args.limit)
                bar.remove_task(task)
                # markup off: an API message with brackets in it is not markup
                bar.console.print(outcome.line(), markup=False, highlight=False)
                outcomes.append(outcome)
    except BrightDataError as exc:
        # Almost always a missing token. The SDK's advice reads as a crash if it
        # arrives under a traceback.
        print(exc, file=sys.stderr)
        return 2

    path = write(outcomes, args.out)
    posts = [post for outcome in outcomes for post in outcome.posts]
    fields = f" ({len(posts[0])} fields per post)" if posts else ""
    print(f"Saved {len(posts)} posts as JSON to {path}{fields}")
    return 0 if all(o.ok for o in outcomes) else 1


if __name__ == "__main__":
    sys.exit(main())
