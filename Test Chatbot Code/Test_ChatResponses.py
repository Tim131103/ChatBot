import unittest
from ChatResponses import ChatResponses

class TestChatResponses(unittest.TestCase):
    def setUp(self):
        # Here you can create an instance of the Chatbot class.
        self.chatresponse = ChatResponses()

    def test_Greeting(self):
        # Example of a test case
        # Arrange
        expected_response = "Hallo!"

        # Act
        response = self.chatresponse.findChatResponse()

        # Assert
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()