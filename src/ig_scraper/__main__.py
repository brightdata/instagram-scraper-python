"""python -m ig_scraper nasa natgeo"""

from __future__ import annotations

import argparse
import sys

from .scrape import scrape, write


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m ig_scraper",
        description="Scrape recent Instagram posts for one or more handles.",
    )
    parser.add_argument("handles", nargs="+", help="handles, with or without the @")
    parser.add_argument("--limit", type=int, default=5, help="posts per handle (default 5)")
    parser.add_argument("--out", default="instagram.json", help="output file")
    args = parser.parse_args(argv)

    outcomes = scrape(args.handles, limit=args.limit)
    for outcome in outcomes:
        print(outcome.line())

    path = write(outcomes, args.out)
    print(f"wrote {sum(len(o.posts) for o in outcomes)} posts to {path}")
    return 0 if all(o.ok for o in outcomes) else 1


if __name__ == "__main__":
    sys.exit(main())
