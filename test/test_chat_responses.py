import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import unittest
from chat_responses import chat_responses

class test_chat_responses(unittest.TestCase):
    def setUp(self):
        # Here you can create an instance of the Chatbot class.
        self.chatresponse = chat_responses()

    def test_greeting(self):
        # Beispiel eines Testfalls für "greeting"
        # Da die Antwort zufällig ist, testen wir, ob die Antwort im erlaubten Bereich ist
        response = self.chatresponse.find_chat_response("greeting")
        self.assertIn(response, ["Hallo!", "Guten Tag!"])

    def test_goodbye(self):
        # Test für "goodbye"
        response = self.chatresponse.find_chat_response("goodbye")
        self.assertIn(response, ["Tschüß!", "Auf Wiedersehen!"])

    def test_unknown_intent(self):
        # Test für einen unbekannten Intent
        response = self.chatresponse.find_chat_response("unknown")
        self.assertEqual(
            response, "Entschuldigung, ich habe das nicht verstanden.")

    def test_error_intent(self):
        # Test für einen error
        response = self.chatresponse.find_chat_response("error")
        self.assertEqual(
            response, "Entschuldigung, ich habe das nicht verstanden.")
        
        #Verbesserung laut GPT?:
        with self.assertRaises(KeyError) as context:
            self.chat_response.find_chat_response("unknown_intent")
        self.assertEqual(str(context.exception),
                         "Unknown intent: 'unknown_intent' not found in intent mapping.")


if __name__ == '__main__':
    unittest.main()
