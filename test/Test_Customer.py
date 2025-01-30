import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Customer import Customer  # Now import should work

class TestCustomer(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a Customer instance for testing.
        """
        self.customer = Customer(
            name="John Doe",
            customer_id="12345",
            customer_status="Gold",
            email="john.doe@example.com",
            phone_number="555-1234",
            birth_date="1990-01-01",
            address="123 Main St, Anytown, AN"
        )

    def test_customer_initialization(self) -> None:
        """
        Test that the customer attributes are initialized correctly.
        """
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.customer_id, "12345")
        self.assertEqual(self.customer.customer_status, "Gold")
        self.assertEqual(self.customer.email, "john.doe@example.com")
        self.assertEqual(self.customer.phone_number, "555-1234")
        self.assertEqual(self.customer.birth_date, "1990-01-01")
        self.assertEqual(self.customer.address, "123 Main St, Anytown, AN")

    def test_customer_str(self) -> None:
        """
        Test the string representation of the customer.
        """
        expected_str = (
            "Customer Name: John Doe\n"
            "Customer ID: 12345\n"
            "Customer Status: Gold\n"
            "Email: john.doe@example.com\n"
            "Phone Number: 555-1234\n"
            "Birth Date: 1990-01-01\n"
            "Address: 123 Main St, Anytown, AN"
        )
        self.assertEqual(str(self.customer), expected_str)

if __name__ == '__main__':
    unittest.main()