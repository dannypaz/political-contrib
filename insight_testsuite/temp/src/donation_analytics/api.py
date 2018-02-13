import csv

from .contribution_formatter import ContributionFormatter
from .repeat_donors import RepeatDonors

def add_donor(row):
    """
        POST /api/add_repeat_donors

        This route takes a 'row' of streamed information and ingests it through
        the contributions formatter.

        This information will later be used to populate a report w/ export_percentile
    """
    formatter = ContributionFormatter(row)
    RepeatDonors().add_row(formatter)
    return None

def export_repeat_donors(output_path, percentile):
    """
        GET /api/export_percentile

        Returns a list (or in our case generates a report) of all repeated donors
        grouped by contribution and zipcode
    """
    RepeatDonors().export_percentile(output_path, percentile)
    return None


