# Wassup people
# Things we gotta do
#
# 1. pretend the info is stereaming

import argparse
import csv
import os
from pathlib import Path

from donation_analytics.donation_file import DonationFile

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input', help='input file path', action='append')
parser.add_argument('--percentile', help='input file path')
parser.add_argument('--output', help='output file path')
args = parser.parse_args()

print("Starting Data Analytics Project")
print("Input files for donation analytics: {}".format(", ".join(args.input)))
print("Output file for donation analytics: {}".format(args.output))
print("Working in the following directory: {}".format(os.getcwd()))
print("Streaming data into processor")

# These method calls will try to simulate data streaming in our application.
for filepath in args.input:
    print("Processing file: {}".format(filepath))
    donation_file = DonationFile(filepath)
    donation_file.process_file()


