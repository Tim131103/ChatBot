import random

class ChatResponses:
    def __init__(self):
        self.intent_mapping = {
            # Begrüßung
            "greeting": [
                "Hallo! Willkommen zurück! Wie kann ich Ihnen heute weiterhelfen?",
                "Guten Tag! Schön, dass Sie da sind. Was steht heute auf Ihrer Agenda?",
                "Hallo! Wie kann ich Ihnen helfen?",
                "Hi! Willkommen beim BUGLAND Support. Was kann ich für Sie tun?"
            ],

            # Verabschiedung
            "goodbye": [
                "Tschüß! Wir freuen uns darauf, Ihnen bald wieder zu helfen.",
                "Auf Wiedersehen! Wir helfen Ihnen auch gerne das nächste Mal bei Problemen.",
                "Tschüss! Falls Sie weitere Fragen haben, melden Sie sich gerne wieder.",
                "Bis bald! Ich hoffe, ich konnte Ihnen helfen."
            ],

            # Hilfe
            "help": [
                "Ich bin der virtuelle Assistent von BUGLAND und stehe Ihnen für Fragen rund um unsere Produkte zur Verfügung.",
                "Ich kann Ihnen bei häufigen Problemen mit unseren Geräten helfen oder Sie an den richtigen Ansprechpartner weiterleiten.",
                "Falls ich Ihre Frage nicht beantworten kann, erreichen Sie unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de."
            ],

            # Fähigkeiten des Chatbots
            "capabilities": [
                "Ich kann Ihnen Informationen zu unseren Produkten geben, häufige Probleme lösen und Sie an den Kundensupport weiterleiten.",
                "Ich helfe Ihnen mit Anleitungen zur Einrichtung, Wartung und Fehlerbehebung unserer Smart-Home-Geräte.",
                "Ich kann allgemeine Fragen zu Bestellungen, Garantie und Reparaturen beantworten.",
                "Falls ich Ihre Frage nicht direkt beantworten kann, wenden Sie sich bitte an unseren Support unter 040 1234567 oder kundensupport@bugland.de."
            ],


            # Unbekannter Intent
            "unknown": [
                "Entschuldigung, ich habe das nicht ganz mitbekommen. Könnten Sie bitte mehr Details geben oder es anders formulieren?",
                "Es tut mir leid, ich bin mir nicht sicher, wie ich darauf reagieren soll. Vielleicht können Sie es anders ausdrücken oder uns mehr Informationen geben?"
            ],

            # Produktinformationen
            "product_info": [
                "BUGLAND Ltd. bietet innovative Smart-Home-Geräte für Haus und Garten. Unsere Hauptprodukte sind der Cleanbug (Saug- und Wischroboter), die Windowfly (Fensterputzroboter) und der Gardenbeetle (Rasen- und Unkrautroboter).",
                "Unsere Produkte erleichtern die Reinigung und Gartenpflege. Falls Sie detaillierte Fragen haben, kontaktieren Sie bitte unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de."
            ],

            # Spezifische Produktprobleme
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

            # Problemlösung & Support
            "troubleshooting": [
                "Versuchen Sie, das Gerät neu zu starten und die Sensoren zu reinigen.",
                "Falls das Problem weiterhin besteht, hilft Ihnen unser Support unter 040 1234567 oder kundensupport@bugland.de."
            ],
            "spare_parts": [
                "Ersatzteile erhalten Sie über unseren Onlineshop oder autorisierte Händler.",
                "Falls Sie nicht sicher sind, welches Ersatzteil Sie benötigen, kontaktieren Sie unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de."
            ],
            "repair_request": [
                "Für eine Reparatur benötigen wir die Seriennummer Ihres Geräts und eine Fehlerbeschreibung.",
                "Kontaktieren Sie unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de, um eine Reparatur anzufordern."
            ],
            "warranty_info": [
                "Unsere Geräte haben eine Garantie von 2 Jahren auf Material- und Herstellungsfehler.",
                "Bei Garantieanfragen wenden Sie sich bitte an unseren Support: 040 1234567 oder kundensupport@bugland.de."
            ],

            # Beschwerden & Rücksendungen
            "support_complaint": [
                "Es tut uns leid, dass Sie mit unserem Support-Team nicht zufrieden sind. Wir setzen alles daran, den Prozess zu verbessern, und Ihr Feedback hilft uns dabei.",
                "Wir verstehen, dass der Support manchmal frustrierend sein kann. Unser Team wird besser geschult, um Ihre Anliegen schneller und effizienter zu bearbeiten."
            ],
            "product_return": [
                "Die defekten Geräte können nur mit Originalersatzteilen repariert werden. Bitte setzen Sie sich mit unserem Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de in Verbindung, um eine Rücksendung zu arrangieren.",
                "Falls Ihr Gerät defekt ist, können Sie es gerne zur Reparatur einsenden. Denken Sie daran, nur Originalersatzteile werden verwendet, um den Cleanbug oder andere Geräte zu reparieren."
            ],

            # Kundenfeedback
            "customer_feedback": [
                "Ihr Feedback ist uns sehr wichtig! Wir möchten die Qualität unseres Supports kontinuierlich verbessern. Bitte teilen Sie uns mit, wie wir Ihnen besser helfen können.",
                "Vielen Dank für Ihre Rückmeldung! Wir arbeiten daran, den Kundenservice zu optimieren, und schätzen Ihre Unterstützung.",
                "Wir freuen uns über Ihr Feedback! Möchten Sie eine Bewertung abgeben oder Verbesserungsvorschläge mitteilen?",
                "Ihr Feedback hilft uns, unseren Service zu verbessern. Falls Sie uns direkt erreichen möchten, schreiben Sie bitte an kundensupport@bugland.de."
            ],

            # Zahlungen
            "payment_issue": [
                "Falls es Probleme mit der Zahlung gibt, prüfen Sie bitte Ihre Zahlungsmethode oder wenden Sie sich an unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de.",
                "Ich kann Ihnen helfen, falls eine Zahlung fehlgeschlagen ist. Bitte kontaktieren Sie unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de."
            ],

            # Software & Sicherheit
            "software_update": [
                "Unsere Geräte erhalten regelmäßig Software-Updates für neue Funktionen und Verbesserungen. Haben Sie die neueste Version installiert?",
                "Falls Probleme auftreten, prüfen Sie bitte in der App auf Updates oder kontaktieren Sie unseren Support unter 040 1234567 oder kundensupport@bugland.de."
            ],
            "security_concerns": [
                "Unsere Geräte sind mit modernen Sicherheitsfunktionen ausgestattet. Falls Sie Bedenken haben, helfen wir Ihnen gerne weiter.",
                "Für detaillierte Informationen zu Sicherheitsfragen kontaktieren Sie bitte unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de."
            ],

            # Fun-Intents
            "ultimate_answer": [
                "42 – die Antwort auf alles!"
            ],
            "best_programmers": [
                "Jean-Luc, Tim und Lykka – die besten Programmierer der Welt!"
            ]
        }

    # TODO launch
    # Informationen über verschiedene Produkte
        # wofür verwendet man die Roboter jeweils
    # .json "FLASK_APP": "src/UI/app.py" ?????

    def find_chat_response(self, intent):
        if intent in self.intent_mapping:
            response = random.choice(self.intent_mapping[intent])
        else:
            response = "Entschuldigung, ich habe das nicht verstanden. Kontaktieren Sie bitte unseren Support unter 040 1234567 oder per E-Mail an kundensupport@bugland.de."
            raise KeyError(f"Unknown intent: '{
                           intent}' not found in intent mapping.")
        return response


chat_response = ChatResponses()

response = chat_response.find_chat_response("greeting")
