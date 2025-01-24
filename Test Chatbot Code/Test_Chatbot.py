import unittest
from Chatbot import Chatbot

class TestChatbot(unittest.TestCase):
    def setUp(self):
        # Hier kannst du eine Instanz der Chatbot-Klasse erstellen.
        self.chatbot = Chatbot()

    def test_example_method(self):
        # Beispiel für einen Testfall
        # Arrange
        erwartete_antwort = "Hallo, wie kann ich dir helfen?"

        # Act
        antwort = self.chatbot.example_method()

        # Assert
        self.assertEqual(antwort, erwartete_antwort)

    # Weitere Testmethoden hinzufügen...

if __name__ == '__main__':
    unittest.main()