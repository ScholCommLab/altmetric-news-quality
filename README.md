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

Tentative collection date range: March 1 - March 31

### RSS Feed Collection

The following script will run as a cron job on our scholcommlab server during the collection date range. Execution frequency *tbd*.

1. Use [`feedparser`](https://pythonhosted.org/feedparser/) to access each RSS feed and retrieve the latest ("the latest" might differ for each news source) articles into a normalized format.
2. Load saved articles (stored in jsonl/ndjson format) into a dataframe.
3. Append newest articles.
4. Save new dataframe.
5. Write log (update timestamp; venue; new articles)

### Merge results

1. Combine all six spreadsheets into a main dataframe with a unique identifier for each news article.

### Processing RSS Feed Data

1. Clean and extract tags for each article
2. Extract article content for each article and save the HTML representation
   1. Use `newspaper3k` to download and parse each news article
   2. For Popular Science we have to extract the HTML directly from its RSS feed
3. Extract mentioned URLs for each news article and save into a seperate table for mentioned content.