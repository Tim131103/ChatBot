import os   
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.String(50), nullable=False)
    customer_status = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    def __init__(self, name: str, customer_id: str, customer_status: str, email: str, 
                 phone_number: str, birth_date: str) -> None:
        self.name = name
        self.customer_id = customer_id
        self.customer_status = customer_status
        self.email = email
        self.phone_number = phone_number
        self.birth_date = birth_date

    def __str__(self) -> str:
        return (
            f"Customer Name: {self.name}\n"
            f"Customer ID: {self.customer_id}\n"
            f"Customer Status: {self.customer_status}\n"
            f"Email: {self.email}\n"
            f"Phone Number: {self.phone_number}\n"
            f"Birth Date: {self.birth_date}\n"
        )