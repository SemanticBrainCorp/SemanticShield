from faker import Faker
from SemanticShield.fakers.canadian_card_provider import CanadianCardProvider

class DummyData:
    def __init__(self, operation='maks', redact_string='_') -> None:
        #operation
        #   tokenize = replace with token
        #   maks = replace with inauthentic data with the same structure
        #   redact = remove PII, replace with fixed string (default '_')
        self.operation = operation
        self.redact_string = redact_string
        self.fake = Faker()
        self.fake.add_provider(CanadianCardProvider)

        self.index = 0

    def gen_fake_data_tokenize(self, kind: str):
        dummy = f'[{kind} {self.index}]'
        self.index += 1
        return dummy

    def gen_fake_data_dummy(self, kind: str) -> str:
        if kind == 'PERSON':
            dummy = self.fake.name()
        elif kind == 'PHONE_NUMBER':
            #default faker often generates numbers with extension and openai changes these (e.g. x123 => ext. 123)
            #dummy = self.fake.phone_number()
            dummy = self.fake.canada_phone_number()
        elif kind == 'CREDIT_CARD':
            dummy = self.fake.credit_card_number()
        elif kind == 'EMAIL_ADDRESS':
            dummy = self.fake.email()
        elif kind == 'US_BANK_NUMBER':
            dummy = self.fake.bban()
        elif kind == 'IBAN_CODE':
            dummy = self.fake.iban()
        elif kind == 'IP_ADDRESS':
            dummy = self.fake.ipv4()
        elif kind == 'US_SSN':
            dummy = self.fake.ssn()
        elif kind == 'CA_BANK_ACCT':
            dummy = self.fake.canada_bank_acct()
        elif kind == 'CA_PASSPORT':
            dummy = self.fake.canada_passport()
        elif kind == 'CA_SIN':
            dummy = self.fake.canada_sin()
        elif kind == 'ON_DRIVER_LICENSE':
            dummy = self.fake.ontario_driver()
        elif kind == 'OHIP_CARD':
            dummy = self.fake.ohip()
        else:
            dummy = f'[{kind} {self.index}]'
            self.index += 1
        return dummy

    def gen_fake_data(self, kind: str):
        if self.operation == 'tokenize':
            return self.gen_fake_data_tokenize(kind)
        elif self.operation == 'redact':
            return self.redact_string
        else:
            return self.gen_fake_data_dummy(kind)
