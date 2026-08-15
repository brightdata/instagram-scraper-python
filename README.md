# instagram-scraper-python

Recent Instagram posts as JSON, in Python, on the
[Bright Data Scraper API](https://brightdata.com/products/web-scraper).
Posts only, one command.

## Quickstart

Python 3.10 or newer.

```bash
git clone https://github.com/brightdata/instagram-scraper-python
cd instagram-scraper-python
pip install -e .
export BRIGHTDATA_API_TOKEN=your_token
ig-scraper nasa natgeo
```

Get a token from the
[Bright Data control panel](https://brightdata.com/cp/setting/users). The SDK
reads `BRIGHTDATA_API_TOKEN` on its own, from the environment or from a `.env`
file in the working directory. Copy `.env.example` to `.env` if you prefer a
file.

New accounts get
[5,000 free credits a month](https://docs.brightdata.com/general/account/billing-and-pricing/free-tier).

```
Fetching up to 5 recent posts per account, for: nasa, natgeo
Usually one to three minutes each. One credit per post, 5,000 free per month.
asking  @nasa...
got     @nasa: 5 posts
asking  @natgeo...
got     @natgeo: 5 posts

Saved 10 posts as JSON to instagram.json (34 fields per post)
```

In a terminal each `asking` line is a spinner with a running clock. Results
print as they land, so a slow account never holds up the ones already done.

```
--limit N    posts per account, default 5, minimum 1
--out PATH   output file, default instagram.json
```

`python -m ig_scraper` works too.

## The data

A post has 33 to 36 fields. The ones most people want:

```
url  date_posted  description  hashtags  likes  num_comments  user_posted
```

Nothing is hardcoded, so whatever the API returns is what lands in the file.

<details>
<summary>All 34 fields from a real post</summary>

```
alt_text  audio  audio_url  content_id  content_type  date_posted  description
discovery_input  followers  hashtags  images  input  is_paid_partnership
is_verified  latest_comments  likes  num_comments  partnership_details  photos
photos_number  pk  post_content  post_id  posts_count  product_type
profile_image_link  profile_url  shortcode  thumbnail  timestamp  url
user_posted  user_posted_id  videos_duration
```

Descriptions and data types are on the
[dataset page](https://brightdata.com/cp/scrapers/gd_lk5ns7kz21pck8jpis/pdp/overview),
under Dictionary.

</details>

<details>
<summary>A whole output file, from <code>ig-scraper nasa --limit 1</code></summary>

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
            "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-15/772793459_18636729052049152_6974121686374726637_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=1&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=grEScDEM74MQ7kNvwECp2Jf&_nc_oc=AdoLH4ip3sRRJj-liz6nTbO9j4_GnFiU5jQwJqRuElY7tFM85lPbiFP1c8Je_rBmLb4&_nc_zt=23&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQFujA3878SoMqhkPWKdDHAHpBcl7VMdYt9zin_uNNX-Mg&oe=6A84BC6E"
          ],
          "latest_comments": [
            {
              "comments": "\ud83c\udf12\u2728",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/758357029_17897980650553204_5437085398504268449_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=rc9qkg4PrHsQ7kNvwFuAjf_&_nc_oc=AdrpX8i_18YBLxGaL0WqKYTeVW_O4UWH_rHABqxVZICEUt5d9QmZB0o1saT5tu7Kipc&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQEkn3aY5cXzmWxtuQetKcLiou4vhQ4QvTNLohqw3Om-jw&oe=6A84C1C8",
              "comment_id": "17910634605450132",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=17910634605450132"
            },
            {
              "comments": "That full solar eclipse photo is a square image \ud83e\udd23 Way to try and fool us.",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/550663048_18112342603528761_3029463041747249036_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=109&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy45NjAuQzMifQ%3D%3D&_nc_ohc=pyKMX2H7vUkQ7kNvwGd87QX&_nc_oc=AdrUiw_npDQ1ffHS0Hiy9d8nBA-S8EdHswb4sbVlAm9NVXEWrY3C7619OoQgUdZizks&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQEFwhcGBMP-VwPIXhtFw3evp2Xh7_d94Ly3gUe3uNSPNA&oe=6A84B9B5",
              "comment_id": "18210056371360899",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18210056371360899"
            },
            {
              "comments": "Moment's like wow \ud83c\udf12\ud83c\udf11",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/772179509_18169771318427945_5440326374702722968_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=106&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=Go6kJpwYes0Q7kNvwF4ZZZ8&_nc_oc=AdqzeIVU7M1yrTZKV-r8nm9w7QcdUnXun4vTOxYukgJA5cI6KF-ZcDUieI3Fzol45Ug&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQHBFM-zAlGsoIHcQt1H8q6vaGshhRSseY6I67UHrt_V7A&oe=6A84C517",
              "comment_id": "18088614164426718",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18088614164426718"
            },
            {
              "comments": "the beauty of Lady Selene and Lord Helios \ud83c\udf12",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/686169505_17950694382150256_1445502045857295037_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=108&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=nWo78ocLbvIQ7kNvwEUpKVL&_nc_oc=Adreu7U4bEDZXe5267WN81GiOrf9FWdPT4aiEptRx3V_s0hwX9t3Vm_POLO1FAagVtI&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQGFbJygepmUHwkK9XIlOE7VRAEnLYxjQywwmp7FM0eaxQ&oe=6A84E38B",
              "comment_id": "18018740267864487",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18018740267864487"
            },
            {
              "comments": "Wonderful!!\u2764\ufe0f\u2764\ufe0f\u2764\ufe0f",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/684652877_17963487351064587_3892391821334504342_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=107&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=M67tT0ep0_wQ7kNvwH_xehl&_nc_oc=AdpA-fuYWKqUMOu2ODkfVmZy-oqZpkgzupxJMwjCAjCRevP6mCrRPR9MYgUf2qTfvOA&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQGLYJZL3yWbyHsrwsfXQDgzQy_d2CpjIq71Rtiwzuo-Dg&oe=6A84C428",
              "comment_id": "18121775218870323",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18121775218870323"
            },
            {
              "comments": "I found the map of everything",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/758368245_18088150667560194_4264554113805697272_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=101&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=-Q9-E7nGaUMQ7kNvwHAFvtq&_nc_oc=AdpTOQIlM7srIz4K-_wYBZC6lsrAkm-e4e66J3suIMJfA_2is3PseggigVfXEFQ5Ypg&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQHEXPORZd6BlLqndCF-mlOzEbQKByO5upmRMiwbuEr2nw&oe=6A84B6AD",
              "comment_id": "18165950455415519",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18165950455415519"
            },
            {
              "comments": "\ud83d\ude0d\ud83d\ude0d",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/773686653_18091922129107932_4920244446080151994_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=QzzOUlkLLpcQ7kNvwGpjOev&_nc_oc=AdpSGbBWNQByi3IVCklFy17-BQ1--MWC1UMblttV4SyCX3bhpUJjd6FRVN0Yw7-sMqA&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQFdCk1c6_1x2nZzxzr9lJXOYDpghzLnZgiA2XY_ZYuKtA&oe=6A84D951",
              "comment_id": "18012375464954297",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18012375464954297"
            },
            {
              "comments": "fgsdfzg",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/773519852_18079924742408807_4533500914267054426_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=108&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4zMzUuQzMifQ%3D%3D&_nc_ohc=mMEfpvHlAyEQ7kNvwFTcWtE&_nc_oc=AdqgsX5uPLga4E2GIm7FGgGDKTp8Aa4t7DIBVAI5hMb0yFy9N7AFVipsj4SdawWkRqA&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQHFnPi-HcDUoPu6y8kXKz_B-o5yXt5ZRUFKNsyBfU7Gng&oe=6A84BC77",
              "comment_id": "18117869560918310",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18117869560918310"
            },
            {
              "comments": "\ud83c\udf12\ud83c\udf12\ud83c\udf12\ud83c\udf12\ud83c\udf11\ud83c\udf11\u2728\u2728\u2728\ud83d\udc4f\ud83d\udc4f\ud83d\udc4f",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/708300526_17939656962230895_2437486230692148750_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=111&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=wKpIweHhzF8Q7kNvwE567-l&_nc_oc=AdrxZxsbfUUZ-HIC1Gftd8J9zpB7nYleWBtRML9_qS3lJl7_H-3FgXAZ99mITHfzwa4&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQHQcsnt0uEYV8CHjzw-9CfmTJxSM7SojzfJifwKNR-0KA&oe=6A84B455",
              "comment_id": "18142738816489824",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18142738816489824"
            },
            {
              "comments": "\ud83d\udd25\ud83d\udd25\ud83d\udd25\ud83d\udd25",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/774513564_18090722048139067_8136189635586666987_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=108&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=rUhxiNUreOkQ7kNvwFYxnBP&_nc_oc=Adr-qSlXHF4WpYSyWAEQhIcVGJzf8Tig4C77VurCKxrZaIKw6dT0si8Q4dyoi40nkcw&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQGg77pG6hgUyW9NjsxZQ1DpTj-U3QZIAZxzF-dOAbbm8A&oe=6A84BF3C",
              "comment_id": "18142759522485409",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18142759522485409"
            },
            {
              "comments": "\u2764\ufe0f",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/724164294_17977341765023768_1772021140273108056_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=100&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDc0LkMzIn0%3D&_nc_ohc=mn1XepS2Hw4Q7kNvwETVRI4&_nc_oc=Adru0v1rfPM7hz-XvpZvBW7LHMKDi9Noqy6HrwaDMrXPlloKngtelseyezsg8jF9GDk&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQHmWFG6FlfD3SiUqp2Amf0r7KaEjQ5iCZqjNRc_2fAv8w&oe=6A84C5D8",
              "comment_id": "17883212649479316",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=17883212649479316"
            },
            {
              "comments": "It's amazing and beautifully captured \u2764\ufe0f\ud83d\ude0d\ud83d\udc4f\ud83c\udffb",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/757212428_18057473684561191_1015395619269026881_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=101&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy41MTIuQzMifQ%3D%3D&_nc_ohc=ikN0u_TS8XwQ7kNvwF5EPDB&_nc_oc=Adp89I7mRhJ83cxGhz9nyNCZiyRMWRINemOLklAd71RKLmynK10L1yD6-a5OjtBz7is&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQHDELR1sn05h5vUypklFxU34CDdnPb9ebztgoWcbWQjHA&oe=6A84D836",
              "comment_id": "18331895137261496",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18331895137261496"
            },
            {
              "comments": "This is awesome!",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/753546370_17872228383628927_652096331641324260_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=108&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4yMzQuQzMifQ%3D%3D&_nc_ohc=SAnz24h2MSMQ7kNvwFrz8h1&_nc_oc=AdpqmNQNLqtABDo8g_l2S59ld6OygCfoCq1xdADr1XtcS9wdWdN8Npc84s7AW61dmg8&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQEOjG7rxqk6QqXUTGxmCKyRJslZg9AdjdlIZsLlCdrijA&oe=6A84B43A",
              "comment_id": "17986578999012946",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=17986578999012946"
            },
            {
              "comments": "\ud83d\udc4f\ud83d\ude0d",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/774762022_18079834592417172_2441317831005391841_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=109&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=fiyEjx3VhjUQ7kNvwHFtrpe&_nc_oc=AdpjOd68LP7AuKfW_s3ik0F5WBmS99oKNAl730NacMJHqrRHBhVsZ8DjU1lkS5MCxf4&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQEkFKrYprTA2m1c82Ja4ky4ZSeC49obqM4wnNKdPB1Hpw&oe=6A84DD60",
              "comment_id": "18073129151709294",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=18073129151709294"
            },
            {
              "comments": "Alguna vez tiene k estar acompa\u00f1ada",
              "date_of_comment": "2026-08-14",
              "likes": 0,
              "profile_picture": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-19/766121646_18098177420616136_4622123659831918278_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=108&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=Su0Rb4-Dr_0Q7kNvwGD_5wp&_nc_oc=AdpGoaEiVndTJ0N5TApN9L8fldrg4ouWenlwypdgiLfQSGG9mCD2K9odPfW3q249lGA&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQGm6Tp74OkFsMyz4oPoijSjLHEQSoYYyeMM5b4kHiAw3A&oe=6A84D466",
              "comment_id": "17978376534094358",
              "comment_url": "https://www.instagram.com/p/Db_SePSltfz/?comment_id=17978376534094358"
            }
          ],
          "post_id": "3962967439948830707",
          "discovery_input": {
            "url": "https://www.instagram.com/nasa/",
            "num_of_posts": 1,
            "start_date": "",
            "end_date": "",
            "post_type": ""
          },
          "shortcode": "Db_SePSltfz",
          "content_type": "Image",
          "pk": "3962967439948830707",
          "content_id": "Db_SePSltfz",
          "thumbnail": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-15/772793459_18636729052049152_6974121686374726637_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=1&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=grEScDEM74MQ7kNvwECp2Jf&_nc_oc=AdoLH4ip3sRRJj-liz6nTbO9j4_GnFiU5jQwJqRuElY7tFM85lPbiFP1c8Je_rBmLb4&_nc_zt=23&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQFujA3878SoMqhkPWKdDHAHpBcl7VMdYt9zin_uNNX-Mg&oe=6A84BC6E",
          "product_type": "feed",
          "followers": 104000000,
          "posts_count": 4879,
          "profile_image_link": "https://scontent-phl2-1.cdninstagram.com/v/t51.2885-19/29090066_159271188110124_1152068159029641216_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=1&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=wivQr-1LtJsQ7kNvwFG3xa2&_nc_oc=AdriuIXm1GnDN48QoOhzGdJkzig7ujPm2nuj9xnr6AajmMZ5auZKINyB-IQB0eqS2wc&_nc_zt=24&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_ss=79689&oh=00_AQGGVdVKcp59U1xY8Cd8CokA2_BReOSmM4tyr8WQYlvk7w&oe=6A84B9A9",
          "is_verified": true,
          "is_paid_partnership": null,
          "partnership_details": null,
          "user_posted_id": "528817151",
          "post_content": [
            {
              "index": 0,
              "type": "Photo",
              "url": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-15/772793459_18636729052049152_6974121686374726637_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=1&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=grEScDEM74MQ7kNvwECp2Jf&_nc_oc=AdoLH4ip3sRRJj-liz6nTbO9j4_GnFiU5jQwJqRuElY7tFM85lPbiFP1c8Je_rBmLb4&_nc_zt=23&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQFujA3878SoMqhkPWKdDHAHpBcl7VMdYt9zin_uNNX-Mg&oe=6A84BC6E",
              "id": "3962967439948830707",
              "alt_text": "Photo by NASA on August 13, 2026. May be an image of eclipse and text."
            }
          ],
          "audio": null,
          "profile_url": "https://www.instagram.com/nasa",
          "videos_duration": null,
          "images": [
            {
              "url": "https://scontent-phl2-1.cdninstagram.com/v/t51.82787-15/772793459_18636729052049152_6974121686374726637_n.jpg?stp=dst-jpg_e35_s640x640_tt6&_nc_cat=1&ccb=7-5&_nc_sid=18de74&efg=eyJlZmdfdGFnIjoiRkVFRC5iZXN0X2ltYWdlX3VybGdlbi5DMyJ9&_nc_ohc=grEScDEM74MQ7kNvwECp2Jf&_nc_oc=AdoLH4ip3sRRJj-liz6nTbO9j4_GnFiU5jQwJqRuElY7tFM85lPbiFP1c8Je_rBmLb4&_nc_zt=23&_nc_ht=scontent-phl2-1.cdninstagram.com&_nc_gid=gSQyOPCsmnIJJxZBwBQWfw&_nc_ss=79689&oh=00_AQFujA3878SoMqhkPWKdDHAHpBcl7VMdYt9zin_uNNX-Mg&oe=6A84BC6E",
              "id": "3962967439948830707"
            }
          ],
          "alt_text": "Photo by NASA on August 13, 2026. May be an image of eclipse and text.",
          "photos_number": 1,
          "audio_url": null,
          "timestamp": "2026-08-14T11:00:59.773Z",
          "input": {
            "url": "https://www.instagram.com/p/Db_SePSltfz/"
          }
        }
      ]
    }
  ]
}
```

</details>

## When it fails

| you see | what it means |
| --- | --- |
| `API token required but not found.` | Exit 2, before any request. Set the token. |
| `failed  @name: Sorry, this page isn't available.` | Exit 1. No such account, usually a typo. Comes back in about 15 seconds. |
| `got     @name: 0 posts, the account has no public posts in the period searched` | Exit 0, and correct. The API reports an empty window as an error row. |
| `failed  @name: timeout` | Exit 1. A request gives up after 180 seconds. Run it again. |

Any failure exits 1, so a run is safe to gate a script on.

## How it works

One call per account:

```python
client.search.instagram.posts("https://www.instagram.com/nasa/", num_of_posts=5)
```

There is no second collection step. Discovery already returns the complete
record, 34 fields against 33 from collecting the same post afterwards. The
second call cost another credit per post, added 75 seconds, and returned nothing
for accounts whose recent posts are reels.

Three things that cost time to find:

- A record carries both `shortcode` and `url`. The SDK docstrings list only
  `shortcode`.
- An empty date window arrives as an error row on the input, not an empty list,
  reading "There are no public posts in the profile for the specified period".
  That is a success with no records. The code matches on that message, not on
  `error_code`, because a dead account uses the same code.
- `SyncBrightDataClient` builds its event loop in `__enter__`. Unentered, it
  fails with `AttributeError: 'NoneType' object has no attribute
  'run_until_complete'`, which points nowhere near the cause.

All of it is [scrape.py](src/ig_scraper/scrape.py), under 170 lines.

## Coding agents

Claude Code, Codex and Cursor can fetch this without the Python:

```bash
npm install -g @brightdata/cli
brightdata login
brightdata add mcp --agent claude-code --global
```

Use `--agent codex` or `--agent cursor` for those. Ready-made skills are at
[brightdata/skills](https://github.com/brightdata/skills).

The same CLI does the job in one line, with no agent and no clone:

```bash
brightdata pipelines instagram_posts "https://instagram.com/nasa"
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

Tests need no token. CI runs them on every push, and separately follows this
README's install steps on an empty machine, so the quickstart cannot rot. A
second workflow, started by hand from the Actions tab, runs a real scrape.

## License

MIT.
