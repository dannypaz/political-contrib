from datetime import datetime

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
        """
            Some things to consider:
            1. we only need the first 5 numbers of zipcode
            2. Unique records are name and zipcode (we could hash this)
            3. you can just skip the shit if:
        """

        self.cmte_id = self.row[self.get_column_position('cmte_id')]
        self.name = self.row[self.get_column_position('name')]
        self.zip_code = self.row[self.get_column_position('zip_code')]
        self.transaction_dt = self.row[self.get_column_position('transaction_dt')]
        self.transaction_amt = self.row[self.get_column_position('transaction_amt')]
        self.other_id = self.row[self.get_column_position('other_id')]

    def valid_row(self):
        """
            Finds if a row is 'valid' according to the specifications in the Insight
            Data Engineering requirements.

            A record is 'invalid' if one of the following is true:
            - other_id is empty
            - transaction_dt is malformed
            - zipcode is invalid (fewer than 4 digits, missing)
            - name is invalid (empty, malformed?)
            - if CMTE_ID or TRANSACTION_AMT is empty
        """
        if self.required_columns_present:
            return True
        else:
            return False

    def required_columns_present(self):
        if not (self.other_id and self.zip_code and self.name and self.cmte_id and self.transaction_amt):
            return False
        else:
            return True

    def valid_transaction_date(self):
        datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

        if datetime_object:
            return True
        else:
            return False

    def valid_zipcode(self):
        if len(self.zip_code) < 5:
            return False
        else:
            return True

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



