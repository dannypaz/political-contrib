from datetime import datetime

# author: dannypaz
class ContributionFormatter:
    """
        A class to handle all operations for interpreting lines from the contributions data
        format as provided by the FEC: http://classic.fec.gov/finance/disclosure/ftpdet.shtml
    """

    POSITIONS = {
        'cmte_id': 1,
        'name': 8,
        'zip_code': 11,
        'transaction_dt': 14,
        'transaction_amt': 15,
        'other_id': 16,
    }
    POSITION_OFFSET = 1
    FIELD_DELIMETER = '|'

    def __init__(self, row):
        self.row = self.normalize_row(row)

        self.cmte_id = None
        self.name = None
        self.zip_code = None
        self.transaction_dt = None
        self.transaction_amt = None
        self.other_id = None

        self.parse_row()

    def normalize_row(self, row):
        return "".join(row).split(self.FIELD_DELIMETER)

    def get_column_position(self, column_name):
        return self.POSITIONS[column_name] - self.POSITION_OFFSET

    def parse_row(self):
        self.cmte_id = self.row[self.get_column_position('cmte_id')]
        self.name = self.row[self.get_column_position('name')]
        self.zip_code = self.row[self.get_column_position('zip_code')][:5]
        self.transaction_dt = self.row[self.get_column_position('transaction_dt')]
        self.transaction_amt = self.row[self.get_column_position('transaction_amt')]
        self.other_id = self.row[self.get_column_position('other_id')]

    def valid_row(self):
        """
            Finds if a row is 'valid' according to the specifications in the Insight
            Data Engineering requirements.

            A record is 'invalid' if one of the following is true:
            - other_id is not empty
            - transaction_dt is malformed
            - zipcode is invalid (fewer than 4 digits, missing)
            - name is invalid (empty, malformed?)
            - if CMTE_ID or TRANSACTION_AMT is empty
        """

        validations = [
            self.required_columns_present(),
            self.other_id_empty(),
            self.valid_transaction_date(),
            self.valid_zipcode(),
            self.valid_name()
        ]

        return False if False in validations else True

    def required_columns_present(self):
        return (self.zip_code and self.name and self.cmte_id and self.transaction_amt)

    def other_id_empty(self):
        True if not self.other_id else False

    def valid_transaction_date(self):
        try:
            datetime.strptime(self.transaction_dt, '%m%d%Y')
        except ValueError:
            return False

        return True

    def valid_zipcode(self):
        return len(self.zip_code) >= 5

    def valid_name(self):
        return True

    def dump_row(self):
        return {
            'cmte_id': self.cmte_id,
            'name': self.name,
            'zip_code': self.zip_code,
            'dt': self.transaction_dt,
            'amt': float(self.transaction_amt),
            'other_id': self.other_id,
        }
