"""These run without a token. The client is a stub."""

from __future__ import annotations

import inspect
import json
import sys
import typing
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest
from brightdata import BrightDataError

import ig_scraper.__main__  # noqa: F401  (registers the module for monkeypatching)
from ig_scraper.scrape import EMPTY_WINDOW, Outcome, clean_handle, scrape, write

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
    assert outcome.note == "the account has no public posts in the period searched"


def test_any_other_error_row_fails_the_handle():
    row = {"error": "Page not found", "error_code": "dead_page"}
    outcome = scrape(["nasa"], client=stub([row]))[0]

    assert not outcome.ok
    assert outcome.line() == "failed  @nasa: Page not found"


def test_a_timed_out_request_is_a_failure_not_an_empty_creator():
    timed_out = SimpleNamespace(data=None, success=False, error=None, status="timeout")
    client = SimpleNamespace(
        search=SimpleNamespace(instagram=SimpleNamespace(posts=lambda url, **kw: timed_out)),
    )
    outcome = scrape(["nasa"], client=client)[0]

    assert outcome.line() == "failed  @nasa: timeout"


def test_one_bad_handle_does_not_end_the_run():
    first, second = scrape(["nasa", "not a handle"], client=stub(RuntimeError("boom")))

    assert first.error == "RuntimeError: boom"
    assert not second.ok
    assert [o.handle for o in (first, second)] == ["nasa", "not a handle"]


def test_a_run_writes_what_it_found(tmp_path):
    posts = [{"url": "https://www.instagram.com/p/AAA/", "likes": 12, "user_posted": "nasa"}]
    outcomes = scrape(["@nasa"], limit=1, client=stub(posts))

    assert outcomes[0].line() == "got     @nasa: 1 posts"

    path = write(outcomes, tmp_path / "out.json")
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["handles"] == [{"handle": "nasa", "posts": posts}]
    assert document["generated_at"]


def test_a_client_we_own_gets_entered(monkeypatch):
    """SyncBrightDataClient is unusable until __enter__ builds its event loop."""
    entered = []

    class Fake:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            entered.append(True)
            return stub([])

        def __exit__(self, *exc):
            entered.append(False)
            return False

    monkeypatch.setattr(sys.modules["ig_scraper.scrape"], "SyncBrightDataClient", Fake)
    assert scrape(["nasa"])[0].ok
    assert entered == [True, False]


def test_we_do_not_ask_the_sdk_to_create_zones(monkeypatch):
    """Zone creation needs a payment method and this scraper never uses a zone."""
    seen = {}

    class Fake:
        def __init__(self, **kwargs):
            seen.update(kwargs)

        def __enter__(self):
            return stub([])

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(sys.modules["ig_scraper.scrape"], "SyncBrightDataClient", Fake)
    scrape(["nasa"])
    assert seen.get("auto_create_zones") is False


def fake_cli(monkeypatch, outcome_for):
    """Point the CLI at a client that never exists and a handler we control."""
    cli = sys.modules["ig_scraper.__main__"]
    monkeypatch.setattr(cli, "client_context", lambda: nullcontext(object()))
    monkeypatch.setattr(cli, "scrape_handle", lambda client, handle, limit: outcome_for(handle))
    return cli


def test_the_cli_exit_code_says_whether_every_handle_worked(monkeypatch, tmp_path):
    cli = fake_cli(monkeypatch, lambda h: Outcome(h, posts=[{"url": "x"}]))
    assert cli.main(["nasa", "--out", str(tmp_path / "ok.json")]) == 0

    cli = fake_cli(monkeypatch, lambda h: Outcome(h, error="boom"))
    assert cli.main(["nasa", "--out", str(tmp_path / "bad.json")]) == 1


def test_each_result_prints_before_the_next_handle_starts(monkeypatch, tmp_path, capsys):
    """Holding every result to the end is a worse wait than printing nothing."""
    cli = fake_cli(monkeypatch, lambda h: Outcome(h, posts=[{"url": "x"}]))
    cli.main(["nasa", "natgeo", "--out", str(tmp_path / "o.json")])

    out = capsys.readouterr().out.splitlines()
    assert [ln for ln in out if ln.startswith(("asking", "got"))] == [
        "asking  @nasa...",
        "got     @nasa: 1 posts",
        "asking  @natgeo...",
        "got     @natgeo: 1 posts",
    ]


def test_a_limit_below_one_is_refused_before_any_request(capsys):
    """num_of_posts=0 is money spent on a request nobody meant to make."""
    cli = sys.modules["ig_scraper.__main__"]
    for bad in ("0", "-3"):
        with pytest.raises(SystemExit):
            cli.main(["nasa", "--limit", bad])
    assert "1 or more" in capsys.readouterr().err


def test_a_missing_token_is_a_message_not_a_traceback(monkeypatch, capsys):
    cli = sys.modules["ig_scraper.__main__"]

    def no_token():
        raise BrightDataError("API token required but not found.")

    monkeypatch.setattr(cli, "client_context", no_token)
    assert cli.main(["nasa"]) == 2
    assert "token" in capsys.readouterr().err


def test_the_sdk_contract_the_readme_relies_on():
    """Offline, no token. Every claim the README makes about the SDK, pinned here."""
    from brightdata.scrapers import api_client, workflow
    from brightdata.scrapers.instagram.scraper import InstagramScraper
    from brightdata.scrapers.instagram.search import InstagramSearchScraper

    # All eight endpoints, and the trigger/status/fetch trio on every collect one.
    for name in ("profiles", "posts", "reels", "comments"):
        for suffix in ("", "_trigger", "_status", "_fetch"):
            assert callable(getattr(InstagramScraper, name + suffix, None)), name + suffix
    for name in ("profiles", "posts", "reels", "reels_all"):
        assert callable(getattr(InstagramSearchScraper, name, None)), name
    assert "num_of_posts" in inspect.signature(InstagramSearchScraper.posts).parameters

    # Scrapers go through trigger, progress and snapshot. There is no sync path.
    client = next(c for c in vars(api_client).values() if hasattr(c, "TRIGGER_URL"))
    urls = [v for k, v in vars(client).items() if k.endswith("_URL")]
    assert urls and not any(u.endswith("/scrape") for u in urls), urls

    # Every method accepts a list of URLs, so a batch is one call.
    url = inspect.signature(InstagramScraper.posts).parameters["url"].annotation
    assert any(typing.get_origin(a) is list for a in typing.get_args(url)), url

    # Error rows arrive only because the SDK asks for them. The API default is off.
    executor = next(c for c in vars(workflow).values() if hasattr(c, "execute"))
    for fn in (client.trigger, executor.execute):
        assert inspect.signature(fn).parameters["include_errors"].default is True, fn


def test_the_readme_shows_the_example_file_verbatim():
    sample = (ROOT / "examples" / "sample_output.json").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert sample in readme, "README output block and examples/sample_output.json differ"
