from faker import Faker
from faker.providers import BaseProvider
import exrex

class CanadianCardProvider(BaseProvider):
    def ohip(self) -> str:
        return exrex.getone(r'\b[\d]{4}[-][\d]{3}[-][\d]{3}-[A-Z]{2}\b')
    def ontario_driver(self) -> str:
        return exrex.getone(r'\b[A-Z][\d]{4}[-][\d]{5}[-][\d]{5}\b')
    def canada_passport(self) -> str:
        return exrex.getone(r'\b[A-Z]{2}[\d]{6}\b')
    def canada_sin(self) -> str:
        return exrex.getone(r'\b(\d{3}-\d{3}-\d{3})\b')
    def canada_bank_acct(self) -> str:
        return exrex.getone(r'\b(\d{5}-\d{3}-\d{7})|(\d{9})\b')
    def canada_phone_number(self) -> str:
        return exrex.getone(r'\b\(\d{3}\)-\d{3}-\d{4}\b')
