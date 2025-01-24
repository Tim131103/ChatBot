class Customer:
    def __init__(self, name, customer_id, customer_status, email, phone_number, birth_date, address):
        self.name = name
        self.customer_id = customer_id
        self.customer_status = customer_status  # This could be 'Gold', 'Silver', or 'Bronze'
        self.email = email
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.address = address

    def __str__(self):
        return (f"Customer Name: {self.name}\n"
                f"Customer ID: {self.customer_id}\n"
                f"Customer Status: {self.customer_status}\n"
                f"Email: {self.email}\n"
                f"Phone Number: {self.phone_number}\n"
                f"Birth Date: {self.birth_date}\n"
                f"Address: {self.address}")

# Example usage
customer = Customer(
    name="John Doe",
    customer_id="12345",
    customer_status="Gold",
    email="john.doe@example.com",
    phone_number="555-1234",
    birth_date="1990-01-01",
    address="123 Main St, Anytown, AN"
)

print(customer)