# altmetric-news-quality

> Code and Data

## Methodology

Selected publications and their RSS feeds

| Title | Landing Page | RSS Feed |
| --- | --- | --- |
| Wired (science section) | https://www.wired.com/category/science/ | https://www.wired.com/feed/category/science/latest/rss |
| New York Times (science section) | https://www.nytimes.com/section/science | https://rss.nytimes.com/services/xml/rss/nyt/Science.xml |
| The Guardian (science section) | https://www.theguardian.com/science | https://www.theguardian.com/science/rss |
| Popular Science | https://www.popsci.com/ | https://www.popsci.com/arcio/rss/ |
| Scienceblogs | https://scienceblogs.com | https://scienceblogs.com/rss.xml |
| Scienceline | https://scienceline.org | https://scienceline.org/feed |

**Tentative collection timerange: March 1 - March 31**

### Daily RSS Feed Collection

`scripts/collect_feeds_and_sync.py`

The following script will run as a cron job on our scholcommlab server during the collection date range. New articles will be collected once per day. [`feedparser`](https://pythonhosted.org/feedparser/) is used to access the actual RSS feeds as the library helps to parse various RSS versions.

For each of the six news sources:

1. Download current snapshot of the feed
2. Load saved articles
3. Determine new ones by ID and publication date
4. Write log entry with number of new articles and eventual error messages
5. Append new articles to dataframe and save in `jsonl`

### Merge and normalize results

`scripts/merge_and_normalize.py`

After running the script for the collection timerange, we will normalize and merge the six different RSS feed dumps. `feedparser` already helps to a certain degree, however

1. Combine all six spreadsheets into a main dataframe with a unique identifier for each news article.
2. Clean and extract tags for each article

### Extract article content and mentioned URLs

`scripts/extract_content_and_urls.py`

1. Extract article content for each article and save the HTML representation
   1. Use `newspaper3k` to download and parse each news article
   2. For Popular Science we have to extract the HTML directly from its RSS feed
2. Save each article as a separate HTML file organized by folders for each news source.
3. Extract mentioned URLs for each news article and save into a seperate table for mentioned content.
   1. Columns: `article_id`, `url`
