#!/bin/zsh
set -eux
cat tok2014tweets| cut -f5 |python make_counts.py > twcounts
cat 2004,7-05_nyt_tok|python make_counts.py > nytcounts

cat twcounts | awk -F $'\t' 'BEGIN {OFS = FS} $2 > 100{print}' | sort -t$'\t' -r -g -k2 > twcounts.sort
cat nytcounts | awk -F $'\t' 'BEGIN {OFS = FS} $2 > 100{print}' | sort -t$'\t' -r -g -k2 > nytcounts.sort

# head -2000 twcounts.sort > twcounts.trimmed1
# head -2000 nytcounts.sort > nytcounts.trimmed1

python finalize.py