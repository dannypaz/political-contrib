import csv
import math
from datetime import datetime

class RepeatDonors:
    CONTRIBUTIONS =  {}
    REPEAT_DONORS = {}

    def add_row(self, formatter):
        row = formatter.dump_row()

        unique_id = "".join([row['name'], row['zip_code']]).replace(" ", "")
        rec_id = row['cmte_id']

        self._initialize_recipient(rec_id)

        if unique_id in self.CONTRIBUTIONS[rec_id]:
            self._add_repeat_donor(unique_id, rec_id)
        else:
            self._initialize_contribution(self.CONTRIBUTIONS[rec_id], unique_id)

        self._add_contribution(rec_id, unique_id, row)

        return None

    def export_with_percentile(self, output_path, percentile):
        # Calculate things
        for dude in self.REPEAT_DONORS:
            recips = self.REPEAT_DONORS[dude]
            for recip in recips:
                info = self.CONTRIBUTIONS[recip]

                total = 0.0
                seen_totals = []

                for idx, v in enumerate(info[dude]['totals']):
                    seen_totals.append(v['amt'])
                    total += v['amt']
                    year = datetime.strptime(v['dt'], '%m%d%Y').year

                    row = [
                        recip,
                        v['zip_code'],
                        year,
                        self._percentile(seen_totals, percentile),
                        total,
                        idx + 1,
                    ]
                    self._export_row(output_path, row)

        #row_headers = [rec_id, zip_code, year, amt, total, occurrance]
        return None

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

    def _percentile(self, data, percentile):
        """
            This example was taken from information in https://stackoverflow.com/questions/2374640/how-do-i-calculate-percentiles-with-python-numpy
            AND from the function definition found on wikipedia.

            This will only work if data is sorted.
        """
        size = len(data)
        return sorted(data)[int(math.ceil((size * float(percentile)) / 100)) - 1]

    def _export_row(self, output_path, row):
        with open(output_path, 'a') as res:
            reswriter = csv.writer(res, delimiter='|')
            reswriter.writerow(row)

