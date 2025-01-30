import unittest
import random

# Mocking the random.choice method to ensure consistent test results
def mock_choice(seq):
    return seq[0]

class test_chat_responses:
    def __init__(self):
        self.intent_mapping = {
            "greeting": [
                "Hallo! Willkommen zurück! Wie kann ich Ihnen heute weiterhelfen?",
                "Guten Tag! Schön, dass Sie da sind. Was steht heute auf Ihrer Agenda?",
                "Hallo! Wie kann ich Ihnen helfen?",
                "Hi! Willkommen beim BUGLAND Support. Was kann ich für Sie tun?"
            ],
            "goodbye": [
                "Tschüß! Wir freuen uns darauf, Ihnen bald wieder zu helfen.",
                "Auf Wiedersehen! Wir helfen Ihnen auch gerne das nächste Mal bei Problemen.",
                "Tschüss! Falls Sie weitere Fragen haben, melden Sie sich gerne wieder.",
                "Bis bald! Ich hoffe, ich konnte Ihnen helfen."
            ],
            "unknown": [
                "Entschuldigung, ich habe das nicht ganz mitbekommen. Könnten Sie bitte mehr Details geben oder es anders formulieren?",
                "Es tut mir leid, ich bin mir nicht sicher, wie ich darauf reagieren soll. Vielleicht können Sie es anders ausdrücken oder uns mehr Informationen geben?"
            ],
            # Other intents omitted for brevity
        }

    def find_chat_response(self, intent):
        if intent in self.intent_mapping:
            response = random.choice(self.intent_mapping[intent])
        else:
            response = "Entschuldigung, ich habe das nicht verstanden. Schreibe bitte eine Mail an it_service@bugland.de"
            raise KeyError(f"Unknown intent: '{intent}' not found in intent mapping.")
        return response

class TestChatResponses(unittest.TestCase):
    def setUp(self):
        # Patch random.choice to ensure deterministic results
        self.original_choice = random.choice
        random.choice = mock_choice
        self.chatresponse = test_chat_responses()

    def tearDown(self):
        # Restore the original random.choice method
        random.choice = self.original_choice

    def test_greeting(self):
        response = self.chatresponse.find_chat_response("greeting")
        self.assertEqual(response, "Hallo! Willkommen zurück! Wie kann ich Ihnen heute weiterhelfen?")

    def test_goodbye(self):
        response = self.chatresponse.find_chat_response("goodbye")
        self.assertEqual(response, "Tschüß! Wir freuen uns darauf, Ihnen bald wieder zu helfen.")

    def test_unknown_intent(self):
        response = self.chatresponse.find_chat_response("unknown")
        self.assertEqual(response, "Entschuldigung, ich habe das nicht ganz mitbekommen. Könnten Sie bitte mehr Details geben oder es anders formulieren?")

    def test_error_intent(self):
        with self.assertRaises(KeyError) as context:
            self.chatresponse.find_chat_response("unknown_intent")
        self.assertEqual(str(context.exception), "Unknown intent: 'unknown_intent' not found in intent mapping.")

if __name__ == '__main__':
    unittest.main()