from datetime import datetime

# author: dannypaz
class ContributionFormatter:
    """
        A class to handle all operations for interpreting lines from the contributions data
        format as provided by the FEC: http://classic.fec.gov/finance/disclosure/ftpdet.shtml
    """

    # Positions are the same as listed in the FEC format for ftpdet and are NOT
    # indexed to an array (we use a POSITION_OFFSET instead)
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
            - name is invalid (empty)
            - if CMTE_ID or TRANSACTION_AMT is empty

            RE: Name

            A name will be valid if it is not empty. I was going to add function
            calls to check if the name was malformed, but that would either require
            iterating over each character in the name OR using regex.

            For this demo I have decided to use the simplest form
        """

        validations = [
            self.required_columns_present(),
            self.other_id_empty(),
            self.valid_transaction_date(),
            self.valid_zipcode()
        ]

        return False if False in validations else True

    def required_columns_present(self):
        """
            Checks if all 'required' columns are present (non-empty)

            Per product spec, we will only ingest the record if the following fields
            are present. If they are not present, then we will simply tag the record
            as `valid_row` false.

            The consumer (repeat_donors) will then skip the record entirely if `valid_row`
            returns false
        """
        return True if (self.zip_code and self.name and self.cmte_id and self.transaction_amt) else False

    def other_id_empty(self):
        """
            Checks if other_id is empty
        """
        return True if not self.other_id else False

    def valid_transaction_date(self):
        """
            Checks for a valid transaction date IF we can parse the date from the
            format as presented in the FEC documentation.

            We handle the ValueError thrown if the date is in the incorrect format
            and will then return false, not exposing the exception.
        """
        try:
            datetime.strptime(self.transaction_dt, '%m%d%Y')
        except ValueError:
            return False

        return True

    def valid_zipcode(self):
        """
            Checks if the current row's zipcode is atleast 5 characters long
        """
        return len(self.zip_code) >= 5

    def dt_to_year(self, dt):
        """
            Converts a dt string into the current year, used for processing
        """
        return datetime.strptime(dt, '%m%d%Y').year

    def generate_cmte_uuid(self):
        """
            Generates a UUID based off of information on the recipient of a donation.
            This will help us identify contributions based on year.
        """
        year = self.dt_to_year(self.transaction_dt)
        uuid_fields = [self.cmte_id, self.zip_code, str(year)]
        return "".join(uuid_fields)

    def generate_uuid(self):
        """
            Generates a UUID based off of name and zipcode, which will help us
            identify a unique record.
        """
        fields = [self.name, self.zip_code]
        return "".join(fields).replace(" ", "")

    def dump_row(self):
        """
            Returns data for a 'row' that is used by the consumer to generate
            reports.
        """

        return {
            'uuid': self.generate_uuid(),
            'cmte_uuid': self.generate_cmte_uuid(),
            'cmte_id': self.cmte_id,
            'name': self.name,
            'zip_code': self.zip_code,
            'year': self.dt_to_year(self.transaction_dt),
            'amt': int(self.transaction_amt),
        }
