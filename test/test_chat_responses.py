import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from ChatResponses import ChatResponses

class TestChatResponses(unittest.TestCase):
    def setUp(self):
        # Here you can create an instance of the Chatbot class.
        self.chatresponse = ChatResponses()

    def test_greeting(self):
        # Example of a test case
        # Arrange
        expected_response = "Hallo!"

        # Act
        response = self.chatresponse.find_chat_response()

        # Assert
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()