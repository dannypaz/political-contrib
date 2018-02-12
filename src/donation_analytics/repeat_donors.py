import csv
import math
from datetime import datetime

class RepeatDonors:
    CONTRIBUTIONS =  {}
    REPEAT_DONORS = {}

    def add_row(self, formatter):
        """
            Adds a row to the contributions hash (which emulates a datastore)
        """
        if not formatter.valid_row():
            print("Bad row detected and skipped")
            return

        row = formatter.dump_row()

        unique_id = "".join([row['name'], row['zip_code']]).replace(" ", "")
        rec_id = row['cmte_id']

        self._initialize_recipient(rec_id)

        if unique_id in self.CONTRIBUTIONS[rec_id]:
            self._add_repeat_donor(unique_id, rec_id)
        else:
            self._initialize_contribution(self.CONTRIBUTIONS[rec_id], unique_id)

        self._add_contribution(rec_id, unique_id, row)

    def export_with_percentile(self, output_path, percentile):
        """
            Appends rows to a given output path for all repeat donors, updated
            via streaming

            returns None if successful
        """

        for donor in self.REPEAT_DONORS:
            for recip in self.REPEAT_DONORS[donor]:
                self._create_row(recip, donor, percentile, output_path)

    def _create_row(self, recip, donor, percentile, output_path):
        raw_totals = self.CONTRIBUTIONS[recip][donor]['totals']
        total = 0.0
        seen_totals = []

        for idx, v in enumerate(raw_totals):
            seen_totals.append(v['amt'])
            total += v['amt']
            year = datetime.strptime(v['dt'], '%m%d%Y').year

            self._export_row(output_path, [
                recip,
                v['zip_code'],
                year,
                self._percentile(seen_totals, percentile),
                total,
                idx + 1,
            ])

    def _add_contribution(self, rec_id, unique_id, row):
        contrib = self.CONTRIBUTIONS[rec_id][unique_id]
        contrib['totals'].append({
            'amt': row['amt'],
            'dt': row['dt'],
            'zip_code': row['zip_code']
        })

    def _add_repeat_donor(self, unique_id, rec_id):
        if not unique_id in self.REPEAT_DONORS:
            self.REPEAT_DONORS[unique_id] = [rec_id]
        else:
            self.REPEAT_DONORS[unique_id].append(rec_id)

    def _initialize_contribution(self, contributions, unique_id):
        if not unique_id in contributions:
            contributions[unique_id] = {
                'totals': []
            }

    def _initialize_recipient(self, rec_id):
        if not rec_id in self.CONTRIBUTIONS:
            self.CONTRIBUTIONS[rec_id] = {}

    def _percentile(self, totals, percentile):
        """
            This example was taken from information in https://stackoverflow.com/questions/2374640/how-do-i-calculate-percentiles-with-python-numpy
            AND from the function definition found on wikipedia.

            This will only work if data is sorted.
        """
        entries = len(totals)
        return sorted(totals)[int(math.ceil((entries * float(percentile)) / 100)) - 1]

    def _export_row(self, output_path, row):
        """
            Appends a row to a given output path
        """
        with open(output_path, 'a') as res:
            reswriter = csv.writer(res, delimiter='|')
            reswriter.writerow(row)

