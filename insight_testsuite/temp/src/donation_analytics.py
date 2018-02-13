import argparse
import os
from pathlib import Path


from donation_stream.donation_stream import DonationStream


# This file is meant to provide the framework for input file streaming and should
# not be considered a part of the solution
#
# I have stuffed the DonationFile class into this file because it could get confusing
# if this file was a part of the donation_analytics, because it is not required for the
# project, but will make it easier for developers to run and test
#
# author: dannypaz

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
percentile_path = args.percentile
output_path = args.output

for file_path in args.input:
    print("Processing file: {}".format(file_path))
    donation_file = DonationStream(file_path, percentile_path, output_path)
    donation_file.execute_stream()


