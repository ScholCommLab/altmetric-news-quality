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
    feed = feedparser.parse(feeds["nyt"])
    articles = pd.DataFrame(feed["entries"])
    articles["tags"] = articles.tags.map(
        lambda x: [_["term"] for _ in x] if type(x) == list else None
    )
    articles["venue"] = venue
    dfs.append(
        articles.head(samples_per_source)[
            ["venue", "title", "link", "summary", "author", "published", "tags"]
        ]
    )

df = pd.concat(dfs, ignore_index=True)
df.index.name = "id"
df.to_csv(f"../data/sample_{ts}.csv", encoding="utf8")