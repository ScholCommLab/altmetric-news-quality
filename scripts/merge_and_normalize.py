#!/usr/bin/env python

import datetime
from pathlib import Path

import pandas as pd

DATA_DIR = "../data"


def main():
    # data directory
    data_dir = Path(DATA_DIR)
    collection_dir = data_dir / "collection"

    # soad news sources
    news_sources = pd.read_csv(data_dir / "news_sources.csv")

    venue_names = news_sources["short_name"].tolist()
    feed_urls = news_sources["feed_url"].tolist()



if __name__ == "__main__":
    main()
