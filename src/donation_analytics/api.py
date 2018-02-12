import csv

from .contribution_formatter import ContributionFormatter
from .repeat_donors import RepeatDonors

def find_repeat_donors(percentile, row, output_path):
    formatter = ContributionFormatter(row)
    RepeatDonors().add_row(formatter)
    RepeatDonors().export_with_percentile(output_path, percentile)
    return None


