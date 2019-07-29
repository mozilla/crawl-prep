#!/usr/bin/env bash

set -e
set -x

SEED_LIST=$1
SEED_LIST_IS_UNRANKED=$2

if [ "$SEED_LIST_IS_UNRANKED" == "1" ]; then
    ./add-rank-to-unranked-seed-list.sh "$SEED_LIST" > /tmp/ranked_seed_list.csv
else
    cp "$SEED_LIST" /tmp/ranked_seed_list.csv
fi

rm crawl_results.csv || true
cd scrapy_project
scrapy crawl unlimited_depth_max_x_links -o ../crawl_results.csv -a ranked_seed_list_csv=/tmp/ranked_seed_list.csv

exit 0
