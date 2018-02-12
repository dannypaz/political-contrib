import csv

from .contribution_formatter import ContributionFormatter

def repeat_donors(percentile, row, output_path):
    formatter = ContributionFormatter(row)
    row = formatter.dump_row()

    if formatter.valid_row():
        export_row(row, output_path)
    else:
        print("row is not valid")

def export_row(row, output_path):
    with open(output_path, 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|')
        spamwriter.writerow(row)
