from database import db

class ChatLog(db.Model):
    __tablename__ = 'chat_logs'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, customer_id: int, message: str, response: str = None) -> None: # type: ignore
        self.customer_id = customer_id
        self.message = message
        self.response = response

    def __str__(self) -> str:
        return (
            f"ChatLog ID: {self.id}\n"
            f"Customer ID: {self.customer_id}\n"
            f"Message: {self.message}\n"
            f"Response: {self.response}\n"
            f"Timestamp: {self.timestamp}\n"
        )