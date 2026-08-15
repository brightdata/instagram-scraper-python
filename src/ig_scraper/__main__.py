"""ig-scraper nasa natgeo, or python -m ig_scraper nasa natgeo"""

from __future__ import annotations

import argparse
import sys

from brightdata import BrightDataError

from .scrape import client_context, scrape_handle, write


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ig-scraper",
        description="Scrape recent Instagram posts for one or more handles.",
    )
    parser.add_argument("handles", nargs="+", help="handles, with or without the @")
    parser.add_argument("--limit", type=int, default=5, help="posts per handle (default 5)")
    parser.add_argument("--out", default="instagram.json", help="output file")
    args = parser.parse_args(argv)

    outcomes = []
    try:
        with client_context() as client:
            for handle in args.handles:
                # A request takes over a minute. Announce the handle before the
                # wait and report it the moment it lands, so the terminal is
                # never silent and no result is held back for a later handle.
                print(f"...   @{handle}", flush=True)
                outcome = scrape_handle(client, handle, args.limit)
                print(outcome.line(), flush=True)
                outcomes.append(outcome)
    except BrightDataError as exc:
        # Almost always a missing token. The SDK says what to do about it, and
        # that advice reads as a crash if it arrives under a traceback.
        print(exc, file=sys.stderr)
        return 2

    path = write(outcomes, args.out)
    print(f"wrote {sum(len(o.posts) for o in outcomes)} posts to {path}")
    return 0 if all(o.ok for o in outcomes) else 1


if __name__ == "__main__":
    sys.exit(main())
