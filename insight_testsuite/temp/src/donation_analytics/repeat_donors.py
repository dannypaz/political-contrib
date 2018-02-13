import csv
import math
from datetime import datetime

"""
    First things first:

    1. Identify if we have SEEN this person before
    2. If we have
"""
class RepeatDonors:
    CONTRIBUTIONS = {}
    REPEAT_DONORS = []

    def add_row(self, formatter):
        """
            Adds a row to the contributions hash (which emulates a datastore).
        """
        if not formatter.valid_row():
            print("Bad row detected and skipped")
            return

        row = formatter.dump_row()

        uuid = row['uuid']
        cmte_uuid = row['cmte_uuid']

        if cmte_uuid not in self.CONTRIBUTIONS:
            self.CONTRIBUTIONS[cmte_uuid] = []

        if uuid in self.REPEAT_DONORS:
            self.CONTRIBUTIONS[cmte_uuid].append(row)
        else:
            self.REPEAT_DONORS.append(uuid)

    def export_percentile(self, output_path, percentile):
        """
            exports the percentile for all information contained in the CONTRIBUTIONS
            hash which has been populated by add_row.
        """
        for cmte in self.CONTRIBUTIONS:
            total = 0
            seen_totals = []
            idx = 0

            for row in self.CONTRIBUTIONS[cmte]:
                amt = row['amt']

                seen_totals.append(amt)
                total += amt
                idx += 1

                self._export_row(output_path, [
                    row['cmte_id'],
                    row['zip_code'],
                    row['year'],
                    self._percentile(seen_totals, percentile),
                    total,
                    idx,
                ])

        return None

    def _percentile(self, totals, percentile):
        """
            This example was taken from information in https://stackoverflow.com/questions/2374640/how-do-i-calculate-percentiles-with-python-numpy
            AND from the function definition found on wikipedia.

            This will only work if data is sorted.
        """
        entries = len(totals)
        return sorted(totals)[int(math.ceil((entries * int(percentile)) / 100)) - 1]

    def _export_row(self, output_path, row):
        """
            Appends a row to a given output path
        """
        with open(output_path, 'a') as res:
            reswriter = csv.writer(res, delimiter='|')
            reswriter.writerow(row)

