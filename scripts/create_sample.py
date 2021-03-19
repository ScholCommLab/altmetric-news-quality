#!/usr/bin/env python

import datetime
from pathlib import Path

import feedparser
import pandas as pd

# How many samples to user per news source
N_SAMPLES = 10
DATA_DIR = "../data"


def collect_sample():
    # data directory
    script_dir = Path(__file__).parent.absolute()
    data_dir = script_dir.parent / "data"

    # soad news sources
    news_sources = pd.read_csv(data_dir / "news_sources.csv")

    venue_names = news_sources["short_name"].tolist()
    feed_urls = news_sources["feed_url"].tolist()

    ts = datetime.date.today()

    dfs = []
    for venue, rss_feed in zip(venue_names, feed_urls):
        feed = feedparser.parse(rss_feed)
        articles = pd.DataFrame(feed["entries"])
        articles["venue"] = venue
        df = pd.DataFrame()
        df = articles[
            ["venue", "title", "link", "summary", "published"]
        ].copy()
        if "tags" in articles.columns:
            df["tags"] = articles["tags"]
        else:
            df["tags"] = None

        df = df.sample(N_SAMPLES)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df.index.name = "id"

    df.to_csv(data_dir / f"sample_{ts}.csv", encoding="utf8")


if __name__ == "__main__":
    collect_sample()
