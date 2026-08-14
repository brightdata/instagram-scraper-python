"""These run without a token. The client is a stub."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from ig_scraper.scrape import EMPTY_WINDOW, clean_handle, scrape, write

ROOT = Path(__file__).resolve().parents[1]


def stub(discovery):
    """A client whose one Instagram call returns canned rows."""

    def search_posts(url, **kwargs):
        if isinstance(discovery, Exception):
            raise discovery
        return SimpleNamespace(data=discovery)

    return SimpleNamespace(
        search=SimpleNamespace(instagram=SimpleNamespace(posts=search_posts)),
    )


def test_clean_handle_takes_a_handle_an_at_sign_or_a_url():
    assert clean_handle("nasa") == "nasa"
    assert clean_handle("@nasa") == "nasa"
    assert clean_handle("https://www.instagram.com/nasa/") == "nasa"
    with pytest.raises(ValueError):
        clean_handle("not a handle")


def test_an_empty_window_is_zero_records_not_a_failure():
    row = {"error": EMPTY_WINDOW, "error_code": "dead_page", "input": {"url": "x"}}
    outcome = scrape(["nasa"], client=stub([row]))[0]

    assert outcome.ok
    assert outcome.posts == []
    assert outcome.note == "no posts in the requested window"


def test_any_other_error_row_fails_the_handle():
    row = {"error": "Page not found", "error_code": "dead_page"}
    outcome = scrape(["nasa"], client=stub([row]))[0]

    assert not outcome.ok
    assert outcome.line() == "FAIL  @nasa  Page not found"


def test_a_timed_out_request_is_a_failure_not_an_empty_creator():
    timed_out = SimpleNamespace(data=None, success=False, error=None, status="timeout")
    client = SimpleNamespace(
        search=SimpleNamespace(instagram=SimpleNamespace(posts=lambda url, **kw: timed_out)),
    )
    outcome = scrape(["nasa"], client=client)[0]

    assert outcome.line() == "FAIL  @nasa  timeout"


def test_one_bad_handle_does_not_end_the_run():
    first, second = scrape(["nasa", "not a handle"], client=stub(RuntimeError("boom")))

    assert first.error == "RuntimeError: boom"
    assert not second.ok
    assert [o.handle for o in (first, second)] == ["nasa", "not a handle"]


def test_a_run_writes_what_it_found(tmp_path):
    posts = [{"url": "https://www.instagram.com/p/AAA/", "likes": 12, "user_posted": "nasa"}]
    outcomes = scrape(["@nasa"], limit=1, client=stub(posts))

    assert outcomes[0].line() == "OK    @nasa  1 posts"

    path = write(outcomes, tmp_path / "out.json")
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["handles"] == [{"handle": "nasa", "posts": posts}]
    assert document["generated_at"]


def test_a_client_we_own_gets_entered(monkeypatch):
    """SyncBrightDataClient is unusable until __enter__ builds its event loop."""
    entered = []

    class Fake:
        def __enter__(self):
            entered.append(True)
            return stub([])

        def __exit__(self, *exc):
            entered.append(False)
            return False

    monkeypatch.setattr(sys.modules["ig_scraper.scrape"], "SyncBrightDataClient", Fake)
    assert scrape(["nasa"])[0].ok
    assert entered == [True, False]


def test_the_readme_shows_the_example_file_verbatim():
    sample = (ROOT / "examples" / "sample_output.json").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert sample in readme, "README output block and examples/sample_output.json differ"
