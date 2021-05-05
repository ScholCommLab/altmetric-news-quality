# altmetric-news-quality

> Reproduction material and instructions

## Installation

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

## Running stuff (UPDATE)

Most of the scripts should just be fun to be run with `python name_of_script.py`. The daily collection script can also be run from a bash script which we used with a cronjob for automation.

## Methodology

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


**Collection period: March 1 - May 2**

### Raw Data Collection

**RSS Feeds**

`scripts/collect_feeds_and_sync.py`

The following script will run as a cron job on our scholcommlab server during the collection date range. New articles will be collected once per day. [`feedparser`](https://pythonhosted.org/feedparser/) is used to access the actual RSS feeds as the library helps to parse various RSS versions.

For each of the six news sources:

1. Download current snapshot of the feed
2. Load saved articles
3. Determine new ones by ID and publication date
4. Write log entry with number of new articles and eventual error messages
5. Append new articles to dataframe and save in `jsonl`

**Twitter Feeds**

`notebooks/download_twitter_feed.ipynb`

This notebook can be used at any time to collect all tweets from the publications specified in `data/input/twitter_feeds.csv`.

### Preprocess data from both channels

`notebooks/process_channels.py`

This notebook processes each of the two collection processes (e.g., removal of duplicate items, removal of tweets without links) and creates two spreadsheets:

- `data/raw/cleaned_rss.csv`: All items that we identified in the RSS feeds of 6 publications
- `data/raw/cleaned_twitter.csv`: All tweets from two publications that contained a URL to the publications

### Collect metadata for articles

`scripts/extract_content_and_urls.py`

This script uses the previously created cleaned files to create a main spreadsheet with all collected URLs to news articles. Using a combination of meta tags on the publishers pages, custom HTML parsers adjusted to individual sources, and NLP-processing we collect a *publication date*, *section information*, *keywords*, *author information*, and a *title* for every article.

There are various caveats with each field mostly relating to the limitations of normalizing various classifications that are used differently across sources. Sources furthermore use different metadata specifications and standards.

- published: It is unclear how "published date" is used by some sources.
- modified: Not available for three sources.
- section: Again, hard to compare across sources as each source uses these labels differently. In the case of newsmed, only two major sections could be extracted which represent two different topical areas of the publication.
- keywords: Differing granularities of keywords between articles, for some sources the keywords were replaced by tags, and for ifls and healthday the keywords are even derived from the article texts.

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

*Note: MD is meta data extracted from the page header by `newspaper`*
*Note: html indicates content extracted from the page content*
*Note: nlp indicates keyword extraction provided by `newspaper`*

This final notebook creates an output file `data/processes/articles.csv` with news articles published by all 8 sources during the collection period.