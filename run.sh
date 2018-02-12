#!/bin/bash

# Clear out the entire output folder JIC
rm -rf ./output
mkdir output

python ./src/donation-analytics.py --input ./input/itcont.txt --percentile ./input/percentile.txt --output ./output/repeat_donors.txt

