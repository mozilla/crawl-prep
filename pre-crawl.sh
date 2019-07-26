#!/usr/bin/env bash

set -e
set -x

s3cmd --verbose --force get "s3://$S3_BUCKET/$SEED_LIST_PATH" /tmp/seed_list.csv

if [ "$SEED_LIST_IS_UNRANKED" == "1" ]; then
    awk '{printf "%d,%s\n", NR, $0}' < /tmp/seed_list.csv > /tmp/ranked_seed_list.csv
else
    cp /tmp/seed_list.csv /tmp/ranked_seed_list.csv
fi

python -m depth_n_link_following_crawl.gather_internal_links /tmp/ranked_seed_list.csv
s3cmd --verbose sync depth_n_link_following_crawl/data/internal_links.json "s3://$S3_BUCKET/$INTERNAL_LINKS_JSON_OUTPUT_PATH"

exit 0
