# Wassup Insight Data Engineering!
# This file is meant to provide the framework for input file streaming and should
# not be considered a part of the solution
#
# I have stuffed the DonationFile class into this file because it could get confusing
# if this file was a part of the donation_analytics, because it is not required for the
# project, but will make it easier for developers to run and test
#

import argparse
import csv
import os
from pathlib import Path

# This is the actual API of the project
from donation_analytics.repeat_donors import repeat_donors

class DonationFile:
    """
        This class is used to simulate the 'streaming' of a file for the insight
        data engineering project.
    """

    SEPARATOR_TYPES = {
        'itcont.txt': '|',
        'percentile.txt': ''
    }

    def __init__(self, file_path, percentile_path, output_path):
        self.file_path = file_path
        self.percentile = self.get_percentile(percentile_path)
        self.output_path = output_path
        self.file_name = self.filename_from_filepath(file_path)

    def separator(self):
        """
            Returns the column separator for a particular file. Will return blank
            if the file type cannot be found in SEPARATOR_TYPES
        """
        if self.file_name in self.SEPARATOR_TYPES:
            return self.SEPARATOR_TYPES[self.file_name]
        else:
            return ''

    def file_exists(self, path):
        """ Checks if the classes' filepath exists on disk """
        return os.path.isfile(path)

    def filename_from_filepath(self, filepath):
        """ Grabs the filename from a provided filepath """
        return filepath.split('/')[:1]

    def get_percentile(self, percentile_path):
        if not self.file_exists(percentile_path):
            print("Files does not exist: {}".format(self.file_path))
            return False

        with open(percentile_path) as percentile:
            reader = csv.reader(percentile)
            return next(reader)[1:]

    def process_input_file(self):
        """
            Utility function to 'stream' data into our donation analytics engine
            for processing

            We will read the file and then 'process' a single line of contribution.

            @param filename [String] relative path to input files
        """
        if not self.file_exists(file_path):
            print("Files does not exist: {}".format(self.file_path))
            return False

        with open(self.file_path) as datafile:
            datareader = csv.reader(datafile)
            for row in datareader:
                repeat_donors(self.percentile, row, self.output_path)


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
    donation_file = DonationFile(file_path, percentile_path, output_path)
    donation_file.process_input_file()


