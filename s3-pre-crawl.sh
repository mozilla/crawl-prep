#!/usr/bin/env bash

set -e
set -x

s3cmd --verbose --force get "s3://$S3_BUCKET/$SEED_LIST_PATH" /tmp/seed_list.csv

./pre-crawl.sh /tmp/seed_list.csv $SEED_LIST_IS_UNRANKED

s3cmd --verbose put pre_crawl_results.csv "s3://$S3_BUCKET/$CRAWL_RESULTS_OUTPUT_PATH"

exit 0
