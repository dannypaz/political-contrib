import csv
import os.path

class DonationFile:
    SEPARATOR_TYPES = {
        'itcont.txt': '|',
        'percentile.txt': ''
    }

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = self.filename_from_filepath(filepath)

    def separator(self):
        """
            Returns the column separator for a particular file. Will return blank
            if the file type cannot be found in SEPARATOR_TYPES
        """
        if self.filename in self.SEPARATOR_TYPES:
            return self.SEPARATOR_TYPES[self.filename]
        else:
            return ''

    def file_exists(self):
        """ Checks if the classes' filepath exists on disk """
        return os.path.isfile(self.filepath)

    def filename_from_filepath(self, filepath):
        """ Grabs the filename from a provided filepath """
        return filepath.split('/')[:1]

    def process_file(self):
        """
            Utility function to 'stream' data into our donation analytics engine
            for processing

            We will read the file and then 'process' a single line of contribution.

            @param filename [String] relative path to input files
        """
        if not self.file_exists():
            print("Files does not exist: {}".format(self.filepath))
            return False

        with open(self.filepath) as datafile:
            datareader = csv.reader(datafile)
            for row in datareader:
                print("".join(row).split('|'))
