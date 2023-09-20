from faker import Faker
from fakers.canadian_card_provider import CanadianCardProvider

class DummyData:
    def __init__(self, use_placeholders = False) -> None:
        #use_placeholders
        #   True = replace with placeholder string
        #   Flase = replace with dummy data
        self.use_placeholders = use_placeholders
        self.fake = Faker()
        self.fake.add_provider(CanadianCardProvider)

        self.index = 0

    def gen_fake_data_placeholder(self, kind: str):
        dummy = f'[{kind} {self.index}]'
        self.index += 1
        return dummy

    def gen_fake_data_dummy(self, kind: str) -> str:
        if kind == 'PERSON':
            dummy = self.fake.name()
        elif kind == 'PHONE_NUMBER':
            dummy = self.fake.phone_number()
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
        if self.use_placeholders:
            return self.gen_fake_data_placeholder(kind)
        else:
            return self.gen_fake_data_dummy(kind)


'''

CA_PASSPORT
CA_SIN
OHIP_CARD
ON_DRIVER_LICENSE
'LOCATION'
'DATE_TIME'

'US_ITIN'
'MEDICAL_LICENSE'
'CRYPTO'
'AU_ABN'
'UK_NHS'
'AU_TFN'
'AU_MEDICARE'
'US_SSN'
'US_DRIVER_LICENSE'
'US_PASSPORT'
'NRP'
'URL'
'SG_NRIC_FIN'
'AU_ACN'
'''