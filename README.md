# instagram-scraper-python

[![Live check](https://github.com/brightdata/instagram-scraper-python/actions/workflows/live.yml/badge.svg)](https://github.com/brightdata/instagram-scraper-python/actions/workflows/live.yml)

Instagram profiles, posts, reels and comments as JSON, in Python. No Instagram
login, no browser. Built on the
[Bright Data Scraper API](https://brightdata.com/products/web-scraper).

Uses the [Bright Data Python SDK](https://github.com/brightdata/sdk-python).
Full API docs:
[Web Scraper API](https://docs.brightdata.com/scraping-automation/web-data-apis/web-scraper-api/overview).

Also here: a one-command CLI for posts, and the
[Bright Data CLI](#coding-agents), which needs no Python at all.

## Quickstart

Python 3.10 or newer.

```bash
pip install brightdata-sdk
export BRIGHTDATA_API_TOKEN=YOUR_API_KEY
```

Get a token from the
[Bright Data control panel](https://brightdata.com/cp/setting/users). A `.env`
file in the project root works too, as long as the virtualenv is inside the
project.

Or skip the token. Run `npx -p @brightdata/cli bdata login` once: it opens a
browser, and the SDK finds the stored credentials on its own. Do that step
yourself before handing a terminal to a coding agent, since agents cannot click
through it. For a coding agent, set `BRIGHTDATA_API_TOKEN` in its environment;
that is the only step it cannot do itself. The same CLI scrapes Instagram directly; see
[Coding agents](#coding-agents).

New accounts get
[5,000 free credits a month](https://docs.brightdata.com/general/account/billing-and-pricing/free-tier).

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    result = client.search.instagram.posts("https://www.instagram.com/nasa/", num_of_posts=5)
    for post in result.data:
        print(post["likes"], post["num_comments"], post["url"])
```

```
2437761 4692 https://www.instagram.com/p/Db9IVmrDvQ4/
104278 902 https://www.instagram.com/reel/DcMXl1IPNtB/
553843 4101 https://www.instagram.com/p/DcOX3hWFiey/
39490 324 https://www.instagram.com/reel/Dc4u1yKPj_s/
119582 1535 https://www.instagram.com/reel/Dc37MPNSAZq/
```

Expect one to three minutes: the API runs a job and the SDK waits for it. One
credit per post.

Pass `auto_create_zones=False` every time. Left on, the SDK tries to create Web
Unlocker and SERP zones on startup, which Instagram scraping never uses and
which fail on accounts without a payment method.

## Or run it as a command

The command in this repo does the same for several accounts and writes one
JSON file.

```bash
pip install git+https://github.com/brightdata/instagram-scraper-python
ig-scraper nasa natgeo
```

```
Fetching up to 5 recent posts per account, for: nasa, natgeo
Usually one to three minutes each. One credit per post, 5,000 free per month.
asking  @nasa...
got     @nasa: 5 posts
asking  @natgeo...
got     @natgeo: 5 posts

Saved 10 posts as JSON to instagram.json (34 fields per post)
```

In a terminal the `asking` lines are replaced by this, updating in place, so
you can see it is working and how long it has been going:

```
⠹ @nasa 0:01:47
```

```
--limit N    posts per account, default 5, minimum 1
--out PATH   output file, default instagram.json
```

`python -m ig_scraper` works too.

Import it instead of running it:

```python
from ig_scraper import scrape

for outcome in scrape(["nasa"], limit=2):
    for post in outcome.posts:
        print(post["likes"], post["num_comments"], post["url"])
```

```
146397 499 https://www.instagram.com/p/DcCUKZoAS8h/
63408 631 https://www.instagram.com/reel/DcCH2ZygIiP/
```

`scrape` never raises for one bad account. Each `Outcome` carries `handle`,
`posts`, `error` and `note`. Check `ok` before reading `posts`:

```python
from ig_scraper import scrape

for outcome in scrape(["nasa", "zz_not_a_real_account_zz"], limit=1):
    if outcome.ok:
        print(f"{outcome.handle}: {len(outcome.posts)} posts")
    else:
        print(f"{outcome.handle} failed: {outcome.error}")
```

```
nasa: 1 posts
zz_not_a_real_account_zz failed: Crawler error: Cannot read properties of null (reading 'pk')
```

An account with nothing recent is a success with no posts. The reason lands in
`note`, not `error`.

## The rest of the API

The CLI covers one endpoint. The SDK has eight. Every snippet below is complete
and needs only `brightdata-sdk`: paste it as is. Every one of them runs in Actions each Monday, a smaller check
runs every other day, and the badge at the top is the latest result.

| you have | want | call |
| --- | --- | --- |
| a profile URL | recent posts | `client.search.instagram.posts(url, num_of_posts=5)` |
| a username | the profile | `client.search.instagram.profiles("nasa")` |
| a profile URL | the profile | `client.scrape.instagram.profiles(url)` |
| a profile URL | recent reels | `client.search.instagram.reels(url, num_of_posts=5, timeout=420)` |
| a profile URL | every reel ever | `client.search.instagram.reels_all(url)`, one credit per reel the account has posted |
| post URLs | those posts | `client.scrape.instagram.posts([url, url])` |
| reel URLs | those reels | `client.scrape.instagram.reels([url])` |
| a post or reel URL | its comments | `client.scrape.instagram.comments(url)`, one credit per comment |

Every one of these is an asynchronous job. The SDK triggers it, polls, and
returns when it is ready. That is why a call takes one to three minutes, and
why there is no faster path in Python. The API's synchronous endpoint, 20 URLs
and a one-minute limit, is raw HTTP only.

Error rows, like the empty-window one above, appear because the SDK asks for
them with `include_errors=true`. The API default is off.

`search` calls return a list in `result.data`. `scrape` calls with one URL
return one record as a dict, and several as a list.

### Two accounts, one job

A list of URLs is one job, not one per account.

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    result = client.search.instagram.posts(
        ["https://www.instagram.com/nasa/", "https://www.instagram.com/natgeo/"], num_of_posts=1
    )
    for post in result.data:
        print(post["user_posted"], post["url"])
```

```
nasa https://www.instagram.com/p/DcOX3hWFiey/
natgeo https://www.instagram.com/reel/Dbru79IAdH-/
```

### Trigger now, fetch later

For anything bigger than a few accounts, do not block a process for an hour.
Trigger, keep the snapshot id, fetch when ready. Snapshots stay downloadable
for 30 days.

```python
import time

from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    job = client.scrape.instagram.posts_trigger("https://www.instagram.com/p/Dc1W1uFj-CW/")
    print("snapshot:", job.snapshot_id)
    while (status := client.scrape.instagram.posts_status(job.snapshot_id)) not in ("ready", "failed"):
        time.sleep(5)
    print("status:", status)
    record = client.scrape.instagram.posts_fetch(job.snapshot_id)[0]
    print("fetched:", record["url"], "likes:", record["likes"])
```

```
snapshot: sd_mtrapflrzynbfyid9
status: ready
fetched: https://www.instagram.com/p/Dc1W1uFj-CW/ likes: 184
```

### A date window

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    result = client.search.instagram.posts(
        "https://www.instagram.com/nasa/",
        num_of_posts=3,
        start_date="08-01-2026",   # MM-DD-YYYY
        end_date="09-07-2026",
    )
    for post in result.data:
        print(post["date_posted"], post["content_type"], post["url"])
```

```
2026-08-12T21:28:58.000Z Image https://www.instagram.com/p/Db9IVmrDvQ4/
2026-08-18T19:37:40.000Z Reel https://www.instagram.com/reel/DcMXl1IPNtB/
2026-08-19T14:11:47.000Z Image https://www.instagram.com/p/DcOX3hWFiey/
```

`post_type="Post"` filters reels out, verified. `post_type="Reel"` returned no
rows in testing even with a reel inside the window, so do not rely on it.
`posts_to_not_include` takes a list of post IDs.

### A profile, by username, no URL

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    profile = client.search.instagram.profiles("nasa").data[0]
    print(profile["account"], "followers:", profile["followers"], "posts:", profile["posts_count"])
```

```
nasa followers: 104387874 posts: 4913
```

### Comments on a post

One credit per comment, so check `num_comments` on the post first.

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    comments = client.scrape.instagram.comments("https://www.instagram.com/p/Dc1W1uFj-CW/").data
    print(len(comments), "comments; first:", repr(comments[0]["comment"][:60]))
```

```
6 comments; first: 'Those two destroyed jazz'
```

### Recent reels

Reels discovery is slower. The default 180-second timeout expired; 420 did not.

```python
from brightdata import SyncBrightDataClient

with SyncBrightDataClient(auto_create_zones=False) as client:
    reels = client.search.instagram.reels("https://www.instagram.com/nasa/", num_of_posts=2, timeout=420)
    for reel in reels.data:
        print(reel["date_posted"], reel["url"])
```

```
2026-08-18T19:37:40.000Z https://www.instagram.com/p/DcMXl1IPNtB/
2026-09-05T01:00:10.000Z https://www.instagram.com/p/Dc4u1yKPj_s/
```

## The data

The fields most people want:

```
url  date_posted  description  hashtags  likes  num_comments  user_posted
```

The code hardcodes no field list. Whatever the API returns lands in the file.

<!-- fields:start -->
<details>
<summary>All 44 fields, with type and description</summary>

Regenerated every day from the dataset schema, via
`client.datasets.instagram_posts.get_metadata()`, so it cannot go stale. A
post carries the fields that apply to it; the sample file has 34
of these 44.

| field | type | description |
| --- | --- | --- |
| `url` | url | The direct URL of the Instagram post |
| `user_posted` | text | Username of the post creator |
| `description` | text | Post text description |
| `hashtags` | array | Hashtags used in the post |
| `num_comments` | number | Number of comments |
| `date_posted` | date | Post publication date |
| `likes` | number | Number of likes on the post |
| `photos` | array | URLs of attached photos, URLs can be expired due to Instagram policy |
| `videos` | array | URLs of attached videos, URLs can be expired due to Instagram policy |
| `location` | array | Geographical location associated with the post |
| `location_details` | object | Detailed geographical location metadata as returned by Instagram |
| `latest_comments` | array | Recent comments on the post |
| `post_id` | text | Unique post identifier |
| `discovery_input` | object | Discovery input values used to trigger the collection |
| `has_handshake` | boolean | Indicates if the post has a handshake (collaborative agreement between accounts) |
| `display_url` | text | Deprecated: previously used as the display URL of the post media |
| `shortcode` | text | The shortcode of the Instagram post, used in the post URL path |
| `content_type` | text | The type of content: Posts or Reels |
| `pk` | text | The primary key of the media content as assigned by Instagram |
| `content_id` | text | The content ID of the media item |
| `engagement_score_view` | number | Video view count used as an engagement score metric |
| `thumbnail` | text | The URL of the post's display image or video thumbnail |
| `video_view_count` | text | The number of views on the video post |
| `product_type` | text | The type of product associated with the post, such as 'clips' for Reels |
| `coauthor_producers` | array | List of co-authors or producers who collaborated on the post |
| `tagged_users` | array | List of users tagged in the post |
| `video_play_count` | number | The number of times the video has been played |
| `followers` | number | Number of followers the post owner has at the time of collection |
| `posts_count` | number | The total count of posts made by the account at the time of collection |
| `profile_image_link` | text | URL linking directly to the Instagram profile image of the post owner |
| `is_verified` | boolean | Indicates whether the post owner's account is verified |
| `is_paid_partnership` | boolean | Indicates whether the post is a sponsored or paid partnership |
| `partnership_details` | object | Details of the paid partnership brand associated with the post |
| `user_posted_id` | text | The Instagram user ID of the account that posted the post |
| `post_content` | array | List of media items (photos or videos) attached to the post, including carousel items |
| `audio` | object | Audio track metadata associated with the post or Reel |
| `profile_url` | url | URL of the Instagram profile that posted the post |
| `videos_duration` | array | List of video durations for each video attached to the post |
| `images` | array | List of image objects attached to the post |
| `alt_text` | text | Accessibility alt text for the post's main image: descriptive text that conveys the meaning of the image for blind or visually impaired users |
| `photos_number` | number | Total number of photos attached to the post |
| `audio_url` | url | Direct URL of the audio track used in the post |
| `thumbnail_array` | array | Deprecated: array of thumbnail URLs for the post media |
| `country` | text | Some profiles are restricted by location. Please set the country code in Alpha-2 format |

</details>
<!-- fields:end -->

<details>
<summary>The start of a real output file, from <code>ig-scraper nasa --limit 1</code></summary>

```json
{
  "generated_at": "2026-08-14T11:01:05.410349+00:00",
  "handles": [
    {
      "handle": "nasa",
      "posts": [
        {
          "url": "https://www.instagram.com/p/Db_SePSltfz/",
          "user_posted": "nasa",
          "description": "A dance of darkness and light\n\nThis composite image shows the total solar eclipse from beginning to end, as seen in San Mill\u00e1n de los Caballeros, Spain on Aug. 12, 2026.\n\nWhile eclipses are beautiful and magical to experience, they're also a great opportunity for science. Total solar eclipses are particularly important because they allow scientists to see a part of the Sun\u2019s atmosphere known as the corona. The corona is too faint to see except when the bright light of the Sun is blocked.\n\nStudying the corona is key to answering important questions about how heat and energy are transferred from the Sun out into the solar wind, the constant stream of particles that the Sun spews into the solar system.\n\nCredit: NASA\n\n#NASA #Sun #SolarEclipse #Moon",
          "hashtags": [
            "#NASA",
            "#Sun",
            "#SolarEclipse",
            "#Moon"
          ],
          "num_comments": 1109,
          "date_posted": "2026-08-13T17:36:02.000Z",
          "likes": 627573,
          "photos": [
  ...
```

The whole file, one post with every field, is
[examples/sample_output.json](examples/sample_output.json).

</details>

## When it fails

| you see | what it means |
| --- | --- |
| `API token required but not found.` | Exit 2, before any request. Set the token. |
| `failed  @name: ...` | Exit 1. No such account, usually a typo. The wording varies: "Sorry, this page isn't available." and "Crawler error: Cannot read properties of null" are both this. |
| `got     @name: 0 posts, the account has no public posts in the period searched` | Exit 0, and correct. The API reports an empty window as an error row. |
| `failed  @name: timeout` | Exit 1. A request gives up after 180 seconds. Run it again. |

Any failure exits 1, so a run is safe to gate a script on.

## Coding agents

No Python, nothing installed. Paste both lines; the first opens a browser once:

```bash
npx -p @brightdata/cli bdata login
npx -p @brightdata/cli bdata pipelines instagram_posts "https://www.instagram.com/p/Db_SePSltfz/"
```

Agent skills for Claude Code, Codex and Cursor:
[brightdata/skills](https://github.com/brightdata/skills).

<details>
<summary>Every Instagram command the CLI has, each run today</summary>

Four types: `instagram_profiles`, `instagram_posts`, `instagram_reels`,
`instagram_comments`. Each takes URLs, prints JSON, and costs one credit per
record. Prefix each command with `npx -p @brightdata/cli`, or install once with
`npm i -g @brightdata/cli`.

```bash
bdata pipelines instagram_profiles "https://www.instagram.com/nasa/" --pretty
```

1 record, 25 fields, 50 seconds. `"account": "nasa"`, `"followers": 104396028`.

```bash
bdata pipelines instagram_posts "https://www.instagram.com/p/Dc1W1uFj-CW/" --format csv -o posts.csv
```

```
Triggered collection with snapshot ID:sd_mtrcu6qpyebqgtcjg
Output written to posts.csv
```

37 seconds. The CSV header carries the same field names as the table below.

```bash
bdata pipelines instagram_reels "https://www.instagram.com/reel/DcMXl1IPNtB/" --pretty
```

1 record, 25 fields, 23 seconds.

```bash
bdata pipelines instagram_comments "https://www.instagram.com/p/Dc1W1uFj-CW/" --pretty
```

5 records, 11 fields, 9 seconds. One credit per comment, so check the post's
`num_comments` first.

`bdata pipelines list` prints every type. `bdata pipelines --help` shows
`--format json|csv|ndjson|jsonl`, `-o FILE` and `--timeout`.

</details>

## Support

Bugs in this repo:
[open an issue](https://github.com/brightdata/instagram-scraper-python/issues).
Anything about the API, your account or your credits:
[Bright Data support](https://brightdata.zendesk.com/hc/en-us/requests/new).

## License

MIT.
