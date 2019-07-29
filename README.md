# crawl-prep

Preliminary work ahead of Web crawl research (list generation, precrawl, analysis)

## Usage instructions

### Preparations

Setup a Python 3 venv with the required modules:

```
./setup-python-venv.sh
```

Activate the Python 3 venv:

```
source venv/bin/activate
```

### Merge toplists

A simple tool to interleave website toplists ensuring that order is meaningfully preserved so much as possible for an arbitrary sample.
This strategy priorities rank of one list for tie breaking and de-duplicates while combining list. It is intended as a utility for preliminary preparation ahead of performing web crawls for research purposes.

```
python list_merge.py
```

Example output:
```
Length of combined ALEXA/TRANCO list: 14556
Verifying that the list is composed of only unique elements: True
The ALEXA list, truncated at 10000 elements, is a complete subset of the final list of 14556 elements: True
The TRANCO list, truncated at 10000 elements, is a complete subset of the final list of 14556 elements: True
```

### Crawl URLs using Scrapy

```
cd scrapy_project
rm crawl_results.csv || true
awk '{printf "%d,%s\n", NR, $0}' < lists/tranco_10k_alexa_10k_union.head10.csv > /tmp/ranked_seed_list.csv
scrapy crawl unlimited_depth_max_x_links -o crawl_results.csv -a ranked_seed_list_csv=/tmp/ranked_seed_list.csv
```

### Crawl URLs

This will crawl through each site of `seed_list.csv` and gather one depth of internal links. The results will be saved in `./data`. 

```
python -m depth_n_link_following_crawl.gather_internal_links seed_list.csv unranked
```

If the seed list argument is omitted, Alexa Top 10 will be used: 
```
python -m depth_n_link_following_crawl.gather_internal_links
```

Run some analysis on the results:

```
python -m depth_n_link_following_crawl.script
python -m depth_n_link_following_crawl.analyze
```

### Crawl URLs script (for containerized deployment)

This will fetch a seed list from S3, crawl through each site and gather one depth of internal links. The results will be saved in S3:

```
export SEED_LIST_PATH='path/to/ranked_seed_list.csv'
export INTERNAL_LINKS_JSON_OUTPUT_PATH='path/to/internal_links.json'
export S3_BUCKET='bucket-name'
export SEED_LIST_IS_UNRANKED='0' # or '1' if the seed list is unranked
./pre-crawl.sh
```
