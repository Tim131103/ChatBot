import sys
import os
import unittest

# Adjust the path to include the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from chat_response import chat_responses  # Ensure the module name is correct

class TestChatResponses(unittest.TestCase):
    def setUp(self):
        # Create an instance of the Chatbot class
        self.chatresponse = chat_responses()

    def test_greeting(self):
        # Test for "greeting"
        response = self.chatresponse.find_chat_response("greeting")
        self.assertIn(response, ["Hallo!", "Guten Tag!"])

    def test_goodbye(self):
        # Test for "goodbye"
        response = self.chatresponse.find_chat_response("goodbye")
        self.assertIn(response, ["Tschüß!", "Auf Wiedersehen!"])

    def test_unknown_intent(self):
        # Test for an unknown intent
        response = self.chatresponse.find_chat_response("unknown")
        self.assertEqual(response, "Entschuldigung, ich habe das nicht verstanden.")

    def test_error_intent(self):
        # Test for an error intent
        with self.assertRaises(KeyError) as context:
            self.chatresponse.find_chat_response("unknown_intent")
        self.assertEqual(str(context.exception), "Unknown intent: 'unknown_intent' not found in intent mapping.")

if __name__ == '__main__':
    unittest.main()