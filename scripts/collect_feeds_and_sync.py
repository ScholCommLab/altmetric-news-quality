#!/usr/bin/env python

import csv
import datetime
from pathlib import Path

import feedparser
import pandas as pd

DATA_DIR = "../data"


class LogWriter:
    """
    Helper class to manage and write the scraping log
    """

    def __init__(self, dir):
        self.file = dir / "log.csv"
        self.fieldnames = ["timestamp", "venue", "new_articles", "error"]

    def update(self, ts, venue, new_articles, error_msg):
        with open(self.file, mode="a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)

            if not self.file.exists():
                writer.writeheader()

            writer.writerow(
                {
                    "timestamp": ts,
                    "venue": venue,
                    "new_articles": new_articles,
                    "error": error_msg,
                }
            )


def main():
    # data directory
    data_dir = Path(DATA_DIR)
    collection_dir = data_dir / "collection"

    # soad news sources
    news_sources = pd.read_csv(data_dir / "news_sources.csv")

    venue_names = news_sources["short_name"].tolist()
    feed_urls = news_sources["feed_url"].tolist()

    log = LogWriter(collection_dir)

    # Iterate over each news source
    for venue, rss_feed in zip(venue_names, feed_urls):
        ts = datetime.datetime.now()
        error_msg = None
        outfile = collection_dir / f"{venue}.jsonl"
        outfile_exists = outfile.exists()

        # Load saved articles
        if outfile_exists:
            old_entries = pd.read_json(outfile, orient="records", lines=True)
            old_entries.published = pd.to_datetime(old_entries.published)
        else:
            old_entries = pd.DataFrame()

        try:
            # Download current snapshot of the feed
            feed = feedparser.parse(rss_feed)
            entries = pd.DataFrame(feed["entries"])
            entries.published = pd.to_datetime(entries.published)

            # Determine new ones by ID and publication date
            if outfile_exists:
                entries = entries[~entries.id.isin(old_entries)]
                entries = entries[entries["published"] > max(old_entries["published"])]
        except Exception as e:
            print(e)
            error_msg = e

        # Write log entry
        n_new_entries = len(entries)
        log.update(ts, venue, n_new_entries, error_msg)

        # Append new articles to dataframe and write to disk
        output = (
            pd.concat([entries, old_entries])
            .drop_duplicates(subset=["id", "published"])
            .sort_values("published")
        )
        output.to_json(
            outfile,
            orient="records",
            lines=True,
            date_format="iso",
        )


if __name__ == "__main__":
    main()
