import unittest
from datetime import datetime

from .contribution_formatter import ContributionFormatter

class TestContributionFormatter(unittest.TestCase):
    cmte = "1234"
    name = "Dan"
    zipcode = "8675309"
    dt = datetime.today().strftime('%m%d%Y')
    amt = "300"
    other_id = ""

    FAKE_ROW = ["{}|||||||{}|||{}|||{}|{}|{}".format(cmte, name, zipcode, dt, amt, other_id)]

    formatter = ContributionFormatter(FAKE_ROW)

    def create_row_with_params(self, cmte, name, zipcode, dt, amt, other_id):
        return ["{}|||||||{}|||{}|||{}|{}|{}".format(cmte, name, zipcode, dt, amt, other_id)]

    def test_normalize_row(self):
        test_row = ["1|2"]
        result = self.formatter.normalize_row(test_row)

        self.assertEqual(result[0], '1')
        self.assertEqual(result[1], '2')

    def test_get_column_position(self):
        """
            Tests if we receive the right column position for cmte_id
        """
        test_column_name = 'cmte_id'
        result = self.formatter.get_column_position(test_column_name)

        self.assertEqual(result, 0)

    def test_valid_row(self):
        result = self.formatter.valid_row()
        self.assertTrue(result)

    def test_valid_row_bad(self):
        test_row = self.create_row_with_params('', '', '', '', '', '')
        bad_formatter = ContributionFormatter(test_row)
        result = bad_formatter.valid_row()
        self.assertFalse(result)

    def test_other_id_empty(self):
        other_id = "1234"
        test_row = self.create_row_with_params('', '', '', '', '', other_id)
        bad_formatter = ContributionFormatter(test_row)
        result = bad_formatter.other_id_empty()
        self.assertFalse(result)

    def test_valid_zipcode(self):
        zipcode = "1234"
        test_row = self.create_row_with_params('', '', zipcode, '', '', '')
        bad_formatter = ContributionFormatter(test_row)
        result = bad_formatter.valid_zipcode()
        self.assertFalse(result)

    def test_valid_transaction_date(self):
        dt = "20170223"
        test_row = self.create_row_with_params('', '', '', dt, '', '')
        bad_formatter = ContributionFormatter(test_row)
        result = bad_formatter.valid_zipcode()
        self.assertFalse(result)

    def test_dt_to_year(self):
        dt = datetime.today().strftime('%m%d%Y')
        result = self.formatter.dt_to_year(dt)
        self.assertEqual(result, datetime.today().year)

    def test_generate_cmte_uuid(self):
        cmte_id = '1234'
        zipcode = '43434'
        dt = datetime.today().strftime('%m%d%Y')
        test_row = self.create_row_with_params(cmte_id, '', zipcode, dt, '', '')
        result = ContributionFormatter(test_row).generate_cmte_uuid()

        expected_uuid = "".join([cmte_id, zipcode, str(datetime.today().year)])
        self.assertEqual(result, expected_uuid)

    def test_generate_uuid(self):
        name = 'DANNY PAZ'
        zipcode = '43434'
        test_row = self.create_row_with_params('', name, zipcode, '', '', '')
        result = ContributionFormatter(test_row).generate_uuid()

        expected_uuid = "".join([name, zipcode]).replace(" ", "")
        self.assertEqual(result, expected_uuid)

    def test_dump_row(self):
        result = self.formatter.dump_row()
        self.assertEqual(result['cmte_id'], self.cmte)
        self.assertEqual(result['name'], self.name)
        self.assertEqual(result['zip_code'], self.zipcode[:5])
        self.assertEqual(result['amt'], int(self.amt))

if __name__ == '__main__':
    unittest.main()
