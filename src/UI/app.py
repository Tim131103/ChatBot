import nltk
import joblib
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chat_response import ChatResponses
from intents import IntentRecognizer
from flask import Flask, render_template, request, jsonify



app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Initialize IntentRecognizer and ChatResponses
recognizer = IntentRecognizer()
chat_response = ChatResponses()

# Load pre-trained model
recognizer.load_model('intent_recognizer.pkl')

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/')
def home():
    """Render the chatbot UI."""
    return render_template('chatbot_ui.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    try:
        # Force parsing JSON even if the content type is not set
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

        return jsonify({'response': response})

    except Exception as e:
        logging.exception("Error handling chat request")
        return jsonify({'error': 'An error occurred processing your request'}), 500


if __name__ == "__main__":
    app.run(debug=True)
