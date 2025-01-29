import nltk
import joblib 

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

class IntentRecognizer:
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('german'))
        self.model = None
        
    def preprocess_text(self,text):
        """
        Preprocessing the input text:
        - tokenize
        - removing of so called stopwords (i.e. 'und', 'aber', etc.)
        - lemmatize (transform words to their base form)
        """
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        print(tokens)
        return " ".join(tokens)
    
    def train(self, training_data):
        """
        Training the model with given training data
        training_data: List of tupels (text, intent)
        """
        texts = [self.preprocess_text(text) for text, intent in training_data]
        intents = [intent for text, intent in training_data]

        self.model = make_pipeline(CountVectorizer(), MultinomialNB())
        self.model.fit(texts, intents)

    # Wichtig für Chatbot Implementierung
    def predict_intent(self, text):
        if self.model is None:
            raise ValueError("Das Modell wurde noch nicht trainiert.")
        processed_text = self.preprocess_text(text)
        return self.model.predict([processed_text])[0]
    
    def save_model(self, filename):
        if self.model is None:
            raise ValueError("Es gibt kein Modell zum Speichern")
        joblib.dump(self.model, filename)
        print(f"Modell wurd in {filename} gespeichert.")

    def load_model(self, filename):
        self.model = joblib.load(filename)
    

training_data = [
    # Begrüßungen
    ("hallo", "begrüßung"),
    ("hi", "begrüßung"),
    ("guten morgen", "begrüßung"),
    ("guten tag", "begrüßung"),
    ("guten abend", "begrüßung"),
    ("hey", "begrüßung"),
    ("moin", "begrüßung"),    
    # Verabschiedung
    ("tschüss", "verabschiedung"),
    ("auf wiedersehen", "verabschiedung"),
    ("bis bald", "verabschiedung"),
    ("bis später", "verabschiedung"),
    ("bye", "verabschiedung"),
    # Cleanbug Problem
    ("mein cleanbug funktioniert nicht", "cleanbug_problem"),
    ("cleanbug startet nicht", "cleanbug_problem"),
    ("cleanbug reagiert nicht", "cleanbug_problem"),
    ("cleanbug bleibt hängen", "cleanbug_problem"),
    ("cleanbug schaltet sich ständig ab", "cleanbug_problem"),
    ("cleanbug zeigt eine fehlermeldung an", "cleanbug_problem"),
    ("cleanbug arbeitet nicht richtig", "cleanbug_problem"),
    ("cleanbug reinigt nicht mehr", "cleanbug_problem"),
    ("cleanbug macht seltsame geräusche", "cleanbug_problem"),
    ("cleanbug hat einen defekt", "cleanbug_problem"),
    ("cleanbug reinigt nicht gründlich", "cleanbug_problem"),
    ("cleanbug hinterlässt streifen", "cleanbug_problem"),
    ("cleanbug steigt die treppen nicht mehr richtig", "cleanbug_problem"),
    ("ich habe ein problem mit cleanbug", "cleanbug_problem"),
    ("cleanbug macht probleme", "cleanbug_problem"),
    ("cleanbug ist kaputt", "cleanbug_problem"),
    ("cleanbug funktioniert nicht wie erwartet", "cleanbug_problem"),
    ("ich bin mit cleanbug nicht zufrieden", "cleanbug_problem"),
    ("cleanbug erfüllt nicht meine erwartungen", "cleanbug_problem"),
    # Windowfly Problem
    ("mein windowfly startet nicht", "windowfly_problem"),
    ("windowfly reagiert nicht auf befehle", "windowfly_problem"),
    ("windowfly bleibt stecken", "windowfly_problem"),
    ("windowfly schaltet sich plötzlich ab", "windowfly_problem"),
    ("windowfly zeigt einen fehler an", "windowfly_problem"),
    ("windowfly öffnet die fenster nicht", "windowfly_problem"),
    ("windowfly schließt die fenster nicht richtig", "windowfly_problem"),
    ("windowfly bewegt sich nicht mehr", "windowfly_problem"),
    ("windowfly macht ein seltsames geräusch", "windowfly_problem"),
    ("windowfly ist zu langsam", "windowfly_problem"),
    ("windowfly reagiert verzögert", "windowfly_problem"),
    ("windowfly verbraucht zu viel strom", "windowfly_problem"),
    ("windowfly reinigt die fenster nicht gründlich", "windowfly_problem"),
    ("windowfly hinterlässt streifen auf den fenstern", "windowfly_problem"),
    ("ich habe ein problem mit windowfly", "windowfly_problem"),
    ("windowfly macht ständig probleme", "windowfly_problem"),
    ("windowfly funktioniert nicht wie beschrieben", "windowfly_problem"),
    ("windowfly ist kaputt", "windowfly_problem"),
    ("ich bin mit windowfly unzufrieden", "windowfly_problem"),
    ("windowfly spinnt schon wieder", "windowfly_problem"),    
    ("windowfly ist total buggy", "windowfly_problem"),
    # Gardenbeetle Problem
    ("gardenbeetle startet nicht", "gardenbeetle_problem"),
    ("gardenbeetle reagiert nicht auf fernbedienung", "gardenbeetle_problem"),
    ("gardenbeetle bleibt im rasen stecken", "gardenbeetle_problem"),
    ("gardenbeetle schaltet sich mitten in der arbeit ab", "gardenbeetle_problem"),
    ("gardenbeetle zeigt einen roten fehler-blitz an", "gardenbeetle_problem"),
    ("gardenbeetle erkennt die gartengrenzen nicht", "gardenbeetle_problem"),
    ("gardenbeetle fährt nicht in die docking-station zurück", "gardenbeetle_problem"),
    ("gardenbeetle mäht ungleichmäßig", "gardenbeetle_problem"),
    ("gardenbeetle lässt zu viel unkraut übrig", "gardenbeetle_problem"),
    ("gardenbeetle ist extrem langsam", "gardenbeetle_problem"),
    ("gardenbeetle verheddert sich im hohen gras", "gardenbeetle_problem"),
    ("gardenbeetle beschädigt die rasenkante", "gardenbeetle_problem"),
    ("gardenbeetle hinterlässt kahle stellen im rasen", "gardenbeetle_problem"),
    ("die messer von gardenbeetle sind stumpf", "gardenbeetle_problem"),
    ("gardenbeetle macht ein schleifendes geräusch", "gardenbeetle_problem"),
    ("die räder von gardenbeetle blockieren", "gardenbeetle_problem"),
    ("der unkrautgreifer von gardenbeetle klemmt", "gardenbeetle_problem"),
    ("gardenbeetle verliert teile während der arbeit", "gardenbeetle_problem"),
    ("der akku von gardenbeetle hält nur 10 minuten", "gardenbeetle_problem"),
    ("gardenbeetle macht was es will", "gardenbeetle_problem"),
    ("gardenbeetle ist total unzuverlässig", "gardenbeetle_problem"),
    ("gardenbeetle funktioniert nicht wie in der werbung", "gardenbeetle_problem"),
    ("ich habe ständig ärger mit gardenbeetle", "gardenbeetle_problem"),
    ("gardenbeetle erkennt steinige böden nicht", "gardenbeetle_problem"),
    ("gardenbeetle kann kein nasses unkraut entfernen", "gardenbeetle_problem"),
    ("gardenbeetle ist ein totaler ausfall", "gardenbeetle_problem"),
    ("gardenbeetle hat einen knacks", "gardenbeetle_problem"),
    # Support Complains
    ("ich fühle mich vom support schlecht behandelt", "support_complains"),     
    ("der support konnte mein problem nicht lösen", "support_complains"),
    ("ich wurde von einer abteilung zur nächsten weitergeleitet", "support_complains"),
    ("der support hat mir keine hilfreiche antwort gegeben", "support_complains"),
    ("ich bin frustriert, weil mein problem immer noch besteht", "support_complains"),
    ("der support hat mir nur standardantworten gegeben", "support_complains"),
    ("ich bin sehr unzufrieden mit dem support", "support_complains"),
    ("der support hat meine erwartungen nicht erfüllt", "support_complains"),
    ("ich habe schlechte erfahrungen mit dem support gemacht", "support_complains"),
    ("der support ist eine katastrophe", "support_complains"),
    ("ich werde nie wieder den support kontaktieren", "support_complains"),
    ("der support ist total nutzlos", "support_complains"),
    ("ich bin sauer auf den support", "support_complains"),
    ("der support hat mich richtig geärgert", "support_complains"),
    ("ich bin total enttäuscht vom support", "support_complains"),
    ("der support hat mir den letzten nerv geraubt", "support_complains"),
    ("der support hat mich richtig wütend gemacht", "support_complains"),
    ("ich bin total sauer auf den support", "support_complains"),  
    # Product Return
    ("ich möchte mein produkt zurückgeben", "product_return"),
    ("wie kann ich eine rückgabe veranlassen?", "product_return"),
    ("ich will das produkt zurückschicken", "product_return"),
    ("kann ich das produkt zurückgeben?", "product_return"),
    ("wie funktioniert die rückgabe?", "product_return"),
    ("das produkt ist defekt, ich möchte es zurückgeben", "product_return"),
    ("das gerät funktioniert nicht, ich will es zurückschicken", "product_return"),
    ("das produkt ist kaputt, wie kann ich es zurückgeben?", "product_return"),
    ("ich habe einen defekt festgestellt, was muss ich tun?", "product_return"),
    ("das produkt ist beschädigt angekommen", "product_return"),
    ("ich habe das falsche produkt erhalten", "product_return"),
    ("das ist nicht das, was ich bestellt habe", "product_return"),
    ("die lieferung war falsch, ich möchte es zurückgeben", "product_return"),
    ("ich habe etwas anderes bekommen als bestellt", "product_return"),
    ("das produkt entspricht nicht der beschreibung", "product_return"),
    ("das produkt gefällt mir nicht, ich möchte es zurückgeben", "product_return"),
    ("ich bin mit dem produkt nicht zufrieden", "product_return"),
    ("das produkt entspricht nicht meinen erwartungen", "product_return"),
    ("ich möchte das produkt zurückgeben, weil es mir nicht gefällt", "product_return"),
    ("ich habe meine meinung geändert, kann ich es zurückschicken?", "product_return"),
    ("das produkt ist mist, ich schick es zurück", "product_return"),
    ("kann ich den kram zurückschicken?", "product_return"),
    ("das ding will ich nicht mehr, was muss ich tun?", "product_return"),
    ("ich bin sauer, ich möchte das produkt zurückgeben", "product_return"),
    ("das produkt ist ein reinfall, ich will es zurückgeben", "product_return"),
    ("ich bin total enttäuscht, ich möchte mein geld zurück", "product_return"),
    # Customer Feedback
    ('ich bin mit meinem kauf sehr zufrieden!', 'customer_feedback'),
    ('das produkt hat meine erwartungen übertroffen.', 'customer_feedback'),
    ('ich hatte probleme mit der lieferung.', 'customer_feedback'),
    ('der kundenservice war nicht hilfreich.', 'customer_feedback'),
    ('ich möchte eine rückerstattung für meinen artikel.', 'customer_feedback'),
    ('die qualität des produkts ist hervorragend.', 'customer_feedback'),
    ('ich bin enttäuscht von der verpackung.', 'customer_feedback'),
    ('die website ist sehr benutzerfreundlich.', 'customer_feedback'),
    ('ich würde das produkt auf jeden fall weiterempfehlen!', 'customer_feedback'),
    ('ich habe lange auf meine bestellung gewartet.', 'customer_feedback'),
    ('das produkt entspricht nicht der beschreibung.', 'customer_feedback'),
    ('ich bin mit dem preis-leistungs-verhältnis zufrieden.', 'customer_feedback'),
    ('die lieferung war schnell und zuverlässig.', 'customer_feedback'),
    ('ich habe einen defekten artikel erhalten.', 'customer_feedback'),
    ('die auswahl an produkten ist großartig!', 'customer_feedback'),
    ('ich finde die rückgabebedingungen fair.', 'customer_feedback'),
    ('ich habe gute erfahrungen mit dem kundenservice gemacht.', 'customer_feedback'),
    ('die bestellung war einfach und unkompliziert.', 'customer_feedback'),
    ('die farben des produkts sind nicht wie abgebildet.', 'customer_feedback'),
    ('ich bin sehr begeistert von meinem kauf!', 'customer_feedback'),
    ('ich habe keine bestätigung für meine bestellung erhalten.', 'customer_feedback'),
    ('die qualität des materials ist nicht gut.', 'customer_feedback'),
    ('ich finde die versandkosten zu hoch.', 'customer_feedback'),
    ('ich habe das produkt innerhalb von zwei tagen erhalten.', 'customer_feedback'),
    ('der artikel war nicht in der richtigen größe.', 'customer_feedback'),
    ('die webseite hat während des bestellvorgangs gehakt.', 'customer_feedback'),
    ('ich würde gerne mehr informationen zu meinem produkt erhalten.', 'customer_feedback'),
    ('das produkt hat eine lange lebensdauer.', 'customer_feedback'),
    ('ich bin mit der kundenbetreuung sehr zufrieden.', 'customer_feedback'),
    ('ich habe das produkt zurückgeschickt, aber noch keine rückerstattung erhalten.', 'customer_feedback'),
    ('die verpackung war umweltfreundlich.', 'customer_feedback'),
    ('ich habe das produkt als geschenk gekauft und es kam gut an.', 'customer_feedback'),
    ('der artikel war nicht verfügbar, obwohl er online angezeigt wurde.', 'customer_feedback'),
    ('ich finde die app sehr praktisch für bestellungen.', 'customer_feedback'),
    ('ich habe eine falsche bestellung erhalten.', 'customer_feedback'),
    ('der artikel war genau wie beschrieben.', 'customer_feedback'),
    ('ich werde wieder hier einkaufen!', 'customer_feedback'),
    ('ich hatte ein problem beim bezahlen.', 'customer_feedback')
]

if __name__ == "__main__":
    recognizer = IntentRecognizer()

    recognizer.train(training_data)

    recognizer.save_model('intent_recognizer.pkl')

    recognizer.load_model('intent_recognizer.pkl')

    #TODO: Ersetzen mit Tests von Lykka
    test_texts = [
        "hi",
        "Kannst du mir Infos zur Windowfly geben?",
        "Tschüss!"
    ]

    for text in test_texts:
        intent = recognizer.predict_intent(text)
        print(f"Text: {text} -> Absicht: {intent}")