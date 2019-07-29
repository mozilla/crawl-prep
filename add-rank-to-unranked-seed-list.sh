#!/usr/bin/env bash

set -e
set -x

SEED_LIST="$1"
awk '{printf "%d,%s\n", NR, $0}' < "$SEED_LIST"

exit 0
