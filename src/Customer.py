class Customer:
    def __init__(self, name: str, customer_id: str, customer_status: str, email: str, 
                 phone_number: str, birth_date: str, address: str) -> None:
        """
        Initialize a new Customer instance.

        :param name: The name of the customer.
        :param customer_id: A unique identifier for the customer.
        :param customer_status: The status of the customer (e.g., Gold, Silver).
        :param email: The email address of the customer.
        :param phone_number: The phone number of the customer.
        :param birth_date: The birth date of the customer.
        :param address: The address of the customer.
        """
        self.name = name
        self.customer_id = customer_id
        self.customer_status = customer_status
        self.email = email
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.address = address

    def __str__(self) -> str:
        """
        Return a string representation of the customer.

        :return: A formatted string with customer details.
        """
        return (
            f"Customer Name: {self.name}\n"
            f"Customer ID: {self.customer_id}\n"
            f"Customer Status: {self.customer_status}\n"
            f"Email: {self.email}\n"
            f"Phone Number: {self.phone_number}\n"
            f"Birth Date: {self.birth_date}\n"
            f"Address: {self.address}"
        )