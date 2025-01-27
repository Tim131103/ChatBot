class ChatResponses:
    def find_chat_response(intent):
        intent = "greeting" #Bsp. greeting ausprobieren

        intent_mapping = {
        "greeting": "Hallo!"
        }

        response = intent_mapping[intent]
        return response
