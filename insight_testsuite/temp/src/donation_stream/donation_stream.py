import csv
import os

# This is the actual API of the project
from donation_analytics.api import add_donor, export_repeat_donors

# I/O class that mimics event streaming for the Insight Data Engineering challenge
#
# author: dannypaz
class DonationStream:
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
        self.output_path = output_path
        self.percentile = self.get_percentile(percentile_path)
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
        """
            Checks if the classes' filepath exists on disk
        """
        return os.path.isfile(path)

    def filename_from_filepath(self, filepath):
        """
            Grabs the filename from a provided filepath
        """
        return filepath.split('/')[:1]

    def get_percentile(self, percentile_path):
        """
            Reads from a specified percentile file and grabs the value
        """
        with open(percentile_path) as percentile:
            reader = csv.reader(percentile)
            return next(reader)[0]

    def execute_stream(self):
        """
            Utility function to 'stream' data into our donation analytics engine
            for processing

            We will read the file and then 'process' a single line of contribution.

            @param filename [String] relative path to input files
        """
        with open(self.file_path) as datafile:
            datareader = csv.reader(datafile)
            for row in datareader:
                add_donor(row)

            export_repeat_donors(self.output_path, self.percentile)
