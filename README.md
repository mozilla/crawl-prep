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

### Crawl URLs

This will crawl through each site of `ranked_seed_list.csv` and gather at most 10 internal links, following random links until at most 10 has been found.

```
./pre-crawl.sh ranked_seed_list.csv
```

Or, if the seed list is unranked (ie just a list of URLs):
```
./pre-crawl.sh unranked_seed_list.csv 1
```

The results will be saved in `pre_crawl_results.csv`.

Note: You can manually add rank to a seed list as per:

```
./add-rank-to-unranked-seed-list.sh unranked_seed_list.csv > ranked_seed_list.csv
```

### Crawl URLs script for containerized deployment

This will fetch a seed list from S3, crawl through each site and gather one depth of internal links. The results will be saved in S3:

```
export SEED_LIST_PATH='path/to/ranked_seed_list.csv'
export CRAWL_RESULTS_OUTPUT_PATH='path/to/pre_crawl_results.csv'
export S3_BUCKET='bucket-name'
export SEED_LIST_IS_UNRANKED='0' # or '1' if the seed list is unranked
./s3-pre-crawl.sh
```
