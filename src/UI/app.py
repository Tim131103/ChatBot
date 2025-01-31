import logging
import os
import sys
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import db
from customer import Customer
from chat_log import ChatLog
from chat_response import ChatResponses
from intents import IntentRecognizer

def create_app():
    # Initialize Flask app
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Secret key for session management
    app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lausemaus13!@localhost:5432/customer_chat_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with app
    db.init_app(app)

    # Initialize IntentRecognizer and ChatResponses
    recognizer = IntentRecognizer()
    chat_response = ChatResponses()

    # Load pre-trained model
    recognizer.load_model('intent_recognizer.pkl')

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Save customer information to the database
            customer = Customer(
                name=request.form['name'],
                customer_id=request.form['customer_id'],
                customer_status=request.form['customer_status'],
                email=request.form['email'],
                phone_number=request.form['phone_number'],
                birth_date=request.form['birth_date']
            )
            db.session.add(customer)
            db.session.commit()

            # Log the user in without checking credentials
            session['logged_in'] = True
            return redirect(url_for('home'))
        return render_template('login.html')

    @app.route('/')
    def home():
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return render_template('chatbot_ui.html')

    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Handle chat messages from the frontend."""
        try:
            data = request.get_json(force=True)
            if not data or 'message' not in data:
                logging.error("Invalid request data: %s", data)
                return jsonify({'error': 'Invalid input data'}), 400

            user_message = data['message']
            logging.info(f"Received message: {user_message}")

            # Predict intent using the recognizer
            intent = recognizer.predict_intent(user_message)
            logging.info(f"Predicted intent: {intent}")

            # Get response from chat_responses
            response = chat_response.find_chat_response(intent)
            logging.info(f"Response: {response}")

            # Save chat log to the database
            chat_log = ChatLog(
                customer_id=1,  # Replace with actual customer ID logic
                message=user_message,
                response=response
            )
            db.session.add(chat_log)
            db.session.commit()

            return jsonify({'response': response})

        except Exception as e:
            logging.exception("Error handling chat request")
            return jsonify({'error': 'An error occurred processing your request'}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)