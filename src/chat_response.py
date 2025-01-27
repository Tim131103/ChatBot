import random


class chat_responses:
    def __init__(self):
        self.intent_mapping = {
            # Begrüßung
            "greeting": ["Hallo!", "Guten Tag!"],

            # Verabschiedung
            "goodbye": ["Tschüß!", "Auf Wiedersehen!"],

            # Unbekannter Intent
            "unknown": ["Entschuldigung, ich habe das nicht verstanden."],

            # Spezifische Produktanfragen
            "cleanbug_problem": [
                "Oh nein! Der Cleanbug sollte problemlos Treppen steigen können. Bitte wenden Sie sich an unseren Support, damit wir Ihnen weiterhelfen können.",
                "Der Cleanbug hat Probleme beim Treppensteigen? Wir empfehlen, die neueste Firmware-Version zu installieren oder den Support zu kontaktieren, falls das Problem weiterhin besteht."
            ],
            "windowfly_problem": [
                "Die Windowfly sollte sich nicht am Fenster festsetzen. Bitte prüfen Sie, ob die Halterung korrekt angebracht ist, und kontaktieren Sie den Support für eine detaillierte Fehlerbehebung.",
                "Wenn sich die Windowfly am Fenster festzieht, könnte dies auf eine Fehlkonfiguration hindeuten. Lassen Sie uns wissen, ob Sie Unterstützung bei der Einrichtung benötigen."
            ],
            "gardenbeetle_problem": [
                "Der Gardenbeetle sollte effektiv den Rasen mähen und Unkraut entfernen. Falls Probleme auftreten, könnte es an einer fehlerhaften Programmierung liegen. Wir helfen Ihnen gerne weiter.",
                "Sollte der Gardenbeetle nicht wie erwartet funktionieren, prüfen Sie, ob alle Sensoren richtig ausgerichtet sind, oder wenden Sie sich an den Support für weitere Hilfe."
            ],
            "support_complaint": [
                "Es tut uns leid, dass Sie mit unserem Support-Team nicht zufrieden sind. Wir setzen alles daran, den Prozess zu verbessern, und Ihr Feedback hilft uns dabei.",
                "Wir verstehen, dass der Support manchmal frustrierend sein kann. Unser Team wird besser geschult, um Ihre Anliegen schneller und effizienter zu bearbeiten."
            ],
            "product_return": [
                "Die defekten Geräte können nur mit Originalersatzteilen repariert werden. Bitte setzen Sie sich mit unserem Support in Verbindung, um eine Rücksendung zu arrangieren.",
                "Falls Ihr Gerät defekt ist, können Sie es gerne zur Reparatur einsenden. Denken Sie daran, nur Originalersatzteile werden verwendet, um den Cleanbug oder andere Geräte zu reparieren."
            ],
            "customer_feedback": [
                "Ihr Feedback ist uns sehr wichtig! Wir möchten die Qualität unseres Supports kontinuierlich verbessern. Bitte teilen Sie uns mit, wie wir Ihnen besser helfen können.",
                "Vielen Dank für Ihre Rückmeldung! Wir arbeiten daran, den Kundenservice zu optimieren, und schätzen Ihre Unterstützung."
            ]
        }

    def find_chat_response(self, intent):
        if intent in self.intent_mapping:
            response = random.choice(self.intent_mapping[intent])
        else:
            # TODO mit Error umgehen?
            # TODO Nachricht an User, dass unknown intent
            response = "Entschuldigung, ich habe das nicht verstanden."
            raise KeyError(f"Unknown intent: '{intent}' not found in intent mapping.")
        return response


chat_response = chat_responses()

response = chat_response.find_chat_response("greeting")
