import unittest
from datetime import datetime

from .repeat_donors import RepeatDonors

class TestRepeatDonors(unittest.TestCase):
    def test_percentile(self):
        totals = [1,2]
        percentile = 50
        result = RepeatDonors()._percentile(totals, percentile)
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
