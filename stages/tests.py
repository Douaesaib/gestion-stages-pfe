from django.test import TestCase
from stages.validators import is_valid_email, is_valid_phone

class ValidatorTests(TestCase):
    def test_valid_emails(self):
        valid_emails = [
            "test@example.com",
            "user.name+tag@domain.co.uk",
            "ahmed.elamrani@etu.uae.ac.ma",
            "entreprise_123@ntt-data.com",
        ]
        for email in valid_emails:
            self.assertTrue(is_valid_email(email), f"Failed for valid email: {email}")

    def test_invalid_emails(self):
        invalid_emails = [
            "plainaddress",
            "#@%^%#$@#$@#.com",
            "@domain.com",
            "Joe Smith <joe@smith.com>",
            "email.domain.com",
            "email@domain@domain.com",
            "email@domain",
        ]
        for email in invalid_emails:
            self.assertFalse(is_valid_email(email), f"Failed for invalid email: {email}")

    def test_valid_phone_numbers(self):
        valid_phones = [
            "0612345678",        # Moroccan standard mobile
            "+212612345678",     # Moroccan international mobile
            "0522123456",        # Moroccan landline
            "+33 6 12 34 56 78", # French format with spaces
            "06-12-34-56-78",    # Dashed format
            "(+212) 612345678",  # Parentheses and spaces
            "123456789",         # Short valid phone
            "123456789012345",   # Max length (15 digits)
        ]
        for phone in valid_phones:
            self.assertTrue(is_valid_phone(phone), f"Failed for valid phone: {phone}")

    def test_invalid_phone_numbers(self):
        invalid_phones = [
            "1234567",           # Too short (< 8 digits)
            "1234567890123456",  # Too long (> 15 digits)
            "06123abc78",        # Contains alphabets
            "+212612+3456",      # Multiple pluses
            "06@1234567",        # Contains special character
            "+",                 # Only plus
            "",                  # Empty
        ]
        for phone in invalid_phones:
            self.assertFalse(is_valid_phone(phone), f"Failed for invalid phone: {phone}")
