# altmetric-news-quality

> Reproduction material and instructions

## Methodology

> **RSS collection: March 1 - May 3**

> **Twitter collection: March 4**

> **News metadata collection: March 5**

A log of all decisions made before and during the data collection process can be found in the [Wiki](https://github.com/ScholCommLab/altmetric-news-quality/wiki).

### Raw Data Collection

8 publications were selected to be collected through two possible distribution channels: RSS for those that maintain functioning feeds and Twitter for the rest.

| Publication              | URL                                                                                | Channel | Details                                                                                                              |
| ------------------------ | ---------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------- |
| New York Times – Science | [https://www.nytimes.com/section/science](https://www.nytimes.com/section/science) | RSS     | [https://rss.nytimes.com/services/xml/rss/nyt/Science.xml](https://rss.nytimes.com/services/xml/rss/nyt/Science.xml) |
| The Guardian – Science   | [https://www.theguardian.com/science](https://www.theguardian.com/science)         | RSS     | [https://www.theguardian.com/science/rss](https://www.theguardian.com/science/rss)                                   |
| Wired – Science          | [https://www.wired.com/category/science/](https://www.wired.com/category/science/) | RSS     | [https://www.wired.com/feed/category/science/latest/rss](https://www.wired.com/feed/category/science/latest/rss)     |
| Popular Science          | [https://www.popsci.com/](https://www.popsci.com/)                                 | Twitter | [https://twitter.com/PopSci](https://twitter.com/PopSci)                                                             |
| IFLScience               | [https://www.iflscience.com/](https://www.iflscience.com/)                         | Twitter | [https://twitter.com/IFLScience](https://twitter.com/IFLScience)                                                     |
| HealthDay                | [https://consumer.healthday.com](https://consumer.healthday.com)                   | RSS     | [https://consumer.healthday.com/feeds/feed.rss](https://consumer.healthday.com/feeds/feed.rss)                       |
| News Medical             | [https://www.news-medical.net/](https://www.news-medical.net/)                     | RSS     | [http://www.news-medical.net/syndication.axd?format=rss](http://www.news-medical.net/syndication.axd?format=rss)     |
| MedPageToday             | [https://www.medpagetoday.com](https://www.medpagetoday.com)                       | RSS     | [https://www.medpagetoday.com/rss/headlines.xml](https://www.medpagetoday.com/rss/headlines.xml)                     |

#### RSS Feeds

[`scripts/collect_feeds_and_sync.py`](scripts/collect_feeds_and_sync.py)

The following script was run as a cron job on our scholcommlab server during the collection date range. [`feedparser`](https://pythonhosted.org/feedparser/) is used to access the actual RSS feeds as the library helps to parse various RSS versions.

#### Twitter Feeds

[`notebooks/1_download_twitter_feed.ipynb`](notebooks/1_download_twitter_feed.ipynb)

This notebook can be used at any time to collect all tweets from the publications specified in [`data/input/twitter_feeds.csv`](data/input/twitter_feeds.csv).

### Preprocess URLs from RSS/Twitter

[`notebooks/2_process_channels.py`](notebooks/2_process_channels.py)

This notebook processes each of the two collection processes (e.g., removal of duplicate items, removal of tweets without links) and creates two spreadsheets:

- [`data/raw/cleaned_rss.csv`](data/raw/cleaned_rss.csv): All items that we identified in the RSS feeds of 6 publications
- [`data/raw/cleaned_twitter.csv`](data/raw/cleaned_twitter.csv): All tweets from two publications that contained a URL to the publications

### Scrape news articles

[`notebooks/3_scrape_articles.py`](notebooks/3_scrape_articles.py)

This script uses the previously created cleaned files to create a main spreadsheet with all collected URLs to news articles. Using a combination of meta tags on the publishers pages, custom HTML parsers adjusted to individual sources, and NLP-processing we collect a *publication date*, *section information*, *keywords*, *author information*, and a *title* for every article.

There are some caveats that need to be considered for each field due to the limitation and challenge of comparing various classifications used in different ways by news sources. While some might attempt to implement best-practices in terms of meta tags others only provide the bare minimum. Therefore, a few remarks for each collected field:

- published: It is unclear how "published date" is used by some sources (published vs last-updated).
- modified: Not available for three sources.
- section: Difficult to compare across sources as each source uses their classifications differently. While some are quite comparable (guardian, nyt, wired), in the case of newsmed, the two available sections derive from their particular model of publication (i.e., "Medical News" & "Life Science News").
- keywords: Again, similar challenges to keywords. However, for some sources the keywords were replaced by tags for a lack of other keywords. Once again, each source might be using tags and keywords differently in their own contexts. ifls and healthday did not provide any keywords or tags, however, using `newspaper` we could derive keywords from the text bodies.

| Source    | published                  | modified                  | section            | keywords | author             |
| --------- | -------------------------- | ------------------------- | ------------------ | -------- | ------------------ |
| guardian  | MD.article.published\_time | MD.article.modified\_time | MD.article.section | MD       | authors            |
| nyt       | MD.article.published\_time | MD.article.modified\_time | MD.article.section | MD       | authors            |
| wired     | html                       | ---                       | html               | MD       | MD.author          |
| popsci    | MD.article.published\_time | MD.article.modified\_time | html               | html     | authors            |
| ifls      | html                       | ---                       | html               | nlp      | html               |
| newsmed   | MD.article.published\_time | MD.article.modified\_time | html               | MD       | html               |
| medpage   | MD.dc.date                 | ---                       | MD.sailthru.topcat | MD       | MD.sailthru.author |
| healthday | MD.article.published\_time | MD.article.modified\_time | MD.article.section | nlp      | html               |

Note: *MD* is meta data extracted from the page header by `newspaper`. *html* indicates content extracted from the page content. *nlp* indicates keyword extraction provided by `newspaper`. *authors* is a field extracted by `newspaper` heuristics.

This final notebook creates an output file [`data/processes/articles.csv`](data/processes/articles.csv) with news articles published by all 8 sources during the collection period.

### Filtering and sampling

**TBA: Exclusion criteria for articles. E.g., Spanish articles in newsmed, publication dates, sections...**

To create the final dataset with articles that were coded, we sampled *TBD* articles from each source and had to exclude articles that were previously used for several intercoder samples (all samples can be found in [`data/samples/`](data/samples/)).

## Reproduction

### Setup the project

This project uses poetry to manage its dependencies. Recommended (and supposedly easiest) way to get our code running:

1. Get a copy of this repository on your machine and cd into the folder
   1. `git clone git@github.com:ScholCommLab/altmetric-news-quality.git`
   2. `cd altmetric-news-quality`
2. Install [pyenv](https://github.com/pyenv/pyenv) to manage your python versions:
   1. `pyenv install 3.8.2` 
   2. `pyenv local 3.8.2` to set your local python version
3. Install [poetry](https://python-poetry.org/) to install dependencies and manage the local virtualenv
   1. `poetry install`
   2. `poetry shell` to activate the virtualenv

*Note:* Make sure to check out the `newspaper3k` [docs](https://github.com/codelucas/newspaper) as the installation might require some additional software installed on your system outside of the Python universe.

*Another note:* On our RHEL machine, I had to also ensure that `libffi-devel` (`libffi-dev` on Ubuntu/Debian) is installed and recompile the Python distro (i.e., `pyenv uninstall 3.8.2` and then `pyenv install 3.8.2` again). Fun!

Lastly, feel free to use the `requirements.txt` to install the requirements as you wish :)