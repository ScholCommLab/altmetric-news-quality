import datetime

import feedparser
import pandas as pd

samples_per_source = 10

ts = datetime.date.today()

feeds = {
    "wired": "https://www.wired.com/feed/category/science/latest/rss",
    "nyt": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "guardian": "https://www.theguardian.com/science/rss",
    "popsci": "https://www.popsci.com/arcio/rss/",
    "scienceblogs": "https://scienceblogs.com/rss.xml",
    "scienceline": "https://scienceline.org/feed/",
}

dfs = []
for venue, rss_feed in feeds.items():
    feed = feedparser.parse(rss_feed)
    articles = pd.DataFrame(feed["entries"])
    articles["venue"] = venue
    df = pd.DataFrame()
    df = articles[["venue", "title", "link", "summary", "author", "published"]].copy()
    if "tags" in articles.columns:
        df["tags"] = articles["tags"]
    else:
        df["tags"] = None

    df = df.sample(samples_per_source)
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
df.index.name = "id"
df.to_csv(f"../data/sample_{ts}.csv", encoding="utf8")