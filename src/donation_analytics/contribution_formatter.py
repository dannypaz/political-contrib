class ContributionFormatter:
    """
        A class to handle all operations for interpreting lines from the contributions data
        format as provided by the FEC: http://classic.fec.gov/finance/disclosure/ftpdet.shtml
    """

    def __init__(self, row):
        self.row = row

        self.cmte_id = None
        self.name = None
        self.zip_code = None
        self.transaction_dt = None
        self.transaction_amt = None
        self.other_id = None

    def parse_row(self):
        """
            Some things to consider:
            1. we only need the first 5 numbers of zipcode
            2. Unique records are name and zipcode (we could hash this)
            3. you can just skip the shit if:
                - other_id is empty
                - transaction_dt is malformed
                - zipcode is invalid (fewer than 4 digits, missing)
                - name is invalid (empty, malformed?)
                - if CMTE_ID or TRANSACTION_AMT is empty
        """

