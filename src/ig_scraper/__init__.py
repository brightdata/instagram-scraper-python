"""An Instagram scraper on Bright Data's Scraper API."""

from .scrape import Outcome, scrape, scrape_handle, write

__all__ = ["Outcome", "scrape", "scrape_handle", "write"]
__version__ = "0.1.0"
