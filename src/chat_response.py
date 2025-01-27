import random

class chat_responses:
    def __init__(self):
        self.intent_mapping = {
            "greeting": ["Hallo!", "Guten Tag!"],
            "goodbye": ["Tschüß!", "Auf Wiedersehen!"],
            "unknown": ["Entschuldigung, ich habe das nicht verstanden."]
        }
    
    
    
    def find_chat_response(self, intent):
        if intent in self.intent_mapping:
            response = random.choice(self.intent_mapping[intent])
            return response
        else :
            raise ValueError(f"Unknown intent: {intent}")
        

chat_response = chat_responses()

response = chat_response.find_chat_response("greeting")
