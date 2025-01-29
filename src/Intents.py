import nltk
import joblib 
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class IntentRecognizer:
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('german'))
        self.model = None
        self.best_params_ = None
        
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
        # print(tokens)
        return " ".join(tokens)
    
    def train(self, training_data, test_size=0.2, random_state=42):
        """
        Training the model with given training data
        training_data: List of tupels (text, intent)
        """
        texts = [self.preprocess_text(text) for text, intent in training_data]
        intents = [intent for text, intent in training_data]

        X_train, X_test, y_train, y_test = train_test_split(
            texts, intents, test_size=test_size, random_state=random_state
        ) 

        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),  # Einzelner Schritt
            ('clf', MultinomialNB())       # Einzelner Schritt
        ])
        
        # Hyperparameter für die Suche
        param_grid = {
            'tfidf__ngram_range': [(1, 1), (1, 2)],  # Unigramme oder Bigramme
            'tfidf__max_features': [1000, 2000],      # Maximale Anzahl an Features
            'clf__alpha': [0.1, 0.5, 1.0]            # Glättungsparameter für Naive Bayes
        }

        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, n_jobs=-1, verbose=1
        )
        grid_search.fit(X_train, y_train)

        self.model = grid_search.best_estimator_
        self.best_params_ = grid_search.best_params_
        
        # Evaluation auf Testdaten
        y_pred = self.model.predict(X_test)
        print("\nKlassifikationsbericht:")
        print(classification_report(y_test, y_pred))
        self.plot_confusion_matrix(y_test, y_pred)

    def plot_confusion_matrix(self, y_true, y_pred):
        """Visualisiert die Konfusionsmatrix."""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Vorhergesagte Absicht')
        plt.ylabel('Tatsächliche Absicht')
        plt.title('Konfusionsmatrix')
        plt.show()

    # Wichtig für Chatbot Implementierung
    def predict_intent(self, text):
        if self.model is None:
            raise ValueError("Das Modell wurde noch nicht trainiert.")
        processed_text = self.preprocess_text(text)
        # print(f"Text: {processed_text} -> Intent: {self.model.predict([processed_text])[0]} ")
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
    ("hallo", "greeting"),
    ("hi", "greeting"),
    ("guten morgen", "greeting"),
    ("guten tag", "greeting"),
    ("guten abend", "greeting"),
    ("hey", "greeting"),
    ("moin", "greeting"),
    ("hallo zusammen", "greeting"),
    ("servus", "greeting"),
    ("wie geht's?", "greeting"),
    ("was geht?", "greeting"),
    ("schönen tag noch", "greeting"),
    ("willkommen", "greeting"),
    ("hi there", "greeting"),
    ("lange nicht gesehen", "greeting"),
    ("freut mich, dich zu sehen", "greeting"),
    ("alles klar?", "greeting"),
    ("hallo, wie läuft's?", "greeting"),
    ("was macht ihr?", "greeting"),
    ("schön, dich zu treffen", "greeting"),
    ("guten morgen allerseits", "greeting"),
    ("hallo, wie geht es dir?", "greeting"),
    ("guten tag, wie kann ich helfen?", "greeting"),
    ("heyyy", "greeting"),  

    # Verabschiedung
    ("tschüss", "goodbye"),
    ("auf wiedersehen", "goodbye"),
    ("bis bald", "goodbye"),
    ("bis später", "goodbye"),
    ("bye", "goodbye"),
    ("mach's gut", "goodbye"),
    ("bis dann", "goodbye"),
    ("schönen tag noch", "goodbye"),
    ("ciao", "goodbye"),
    ("bis zum nächsten mal", "goodbye"),
    ("wir sehen uns", "goodbye"),
    ("auf bald", "goodbye"),
    ("bis zur nächsten unterhaltung", "goodbye"),
    ("take care", "goodbye"),
    ("schau mal wieder vorbei", "goodbye"),
    ("hab einen schönen tag", "goodbye"),
    ("bis gleich", "goodbye"),
    ("bis zur nächsten woche", "goodbye"),
    ("hab eine gute zeit", "goodbye"),
    ("gute reise", "goodbye"),
    ("mach's besser", "goodbye"),
    ("ich muss jetzt gehen", "goodbye"),
    ("wir sprechen uns später", "goodbye"),
    ("alles gute", "goodbye"),
    ("bis zum nächsten mal", "goodbye"),
    ("auf ein baldiges wiedersehen", "goodbye"),
    ("tschau", "goodbye"),
    ("tschüssie", "goodbye"),
    ("tschö mit ö", "goodbye"),
    ("tschau bella", "goodbye"),
    ("tschüssikowski", "goodbye"),

    # Hilfe
    ('was kannst du für mich tun?', 'help'),
    ('wie kannst du mir helfen?', 'help'),
    ('was macht dieser chatbot?', 'help'),
    ('kannst du mir erklären, was deine funktionen sind?', 'help'),
    ('was sind deine aufgaben als chatbot?', 'help'),
    ('wie funktioniert dieser chatbot?', 'help'),
    ('was kannst du mir über produkte sagen?', 'help'),
    ('kannst du mir bei bestellungen helfen?', 'help'),
    ('was sind die vorteile, mit dir zu sprechen?', 'help'),
    ('wie kannst du mir bei meinen fragen helfen?', 'help'),
    ('was kannst du über bugland ltd. erzählen?', 'help'),
    ('hilfst du mir, produkte zu finden?', 'help'),
    ('was kannst du mir über den kundenservice sagen?', 'help'),
    ('was sind deine hauptfunktionen?', 'help'),
    ('kannst du mir bei problemen mit meiner bestellung helfen?', 'help'),
    ('wie kannst du mich unterstützen?', 'help'),
    ('was sind die häufigsten fragen, die du beantworten kannst?', 'help'),
    ('was kann ich von dir erwarten?', 'help'),
    ('wie hilfst du mir, informationen zu finden?', 'help'),
    ('was ist dein hauptzweck?', 'help'),
    ('kannst du mir tipps geben, wie ich die website nutzen kann?', 'help'),
    ('was kannst du mir über die rückgabebedingungen sagen?', 'help'),
    ('wie kannst du mir bei der produktauswahl helfen?', 'help'),
    ('was sind die ersten schritte, die ich mit dir machen kann?', 'help'),
    ('bist du in der lage, mir bei technischen fragen zu helfen?', 'help'),
    ('wie kannst du mir bei der kontoverwaltung helfen?', 'help'),
    ('was sind die wichtigsten funktionen, die du hast?', 'help'),
    ('kannst du mir sagen, wie ich kontakt zum kundenservice aufnehmen kann?', 'help'),
    ('was sind die häufigsten anfragen, die du bearbeitest?', 'help'),
    ('wie hilfst du mir, die besten angebote zu finden?', 'help'),


    # Produkt Info
    ('was für produkte bietet bugland ltd. an?', 'product_info'),
    ('könntest du mir sagen, welche artikel bugland ltd. verkauft?', 'product_info'),
    ('ich möchte wissen, welche produkte ihr im sortiment habt.', 'product_info'),
    ('gibt es eine liste der produkte von bugland ltd.?', 'product_info'),
    ('was kann ich bei bugland ltd. kaufen?', 'product_info'),
    ('habt ihr spezielle produkte von bugland ltd.?', 'product_info'),
    ('ich interessiere mich für das angebot von bugland ltd.', 'product_info'),
    ('was sind die neuesten produkte von bugland ltd.?', 'product_info'),
    ('kannst du mir mehr über die produkte von bugland ltd. erzählen?', 'product_info'),
    ('ich suche nach informationen über bugland ltd. produkte.', 'product_info'),
    ('gibt es besondere aktionen für produkte von bugland ltd.?', 'product_info'),
    ('was sind die beliebtesten produkte bei bugland ltd.?', 'product_info'),
    ('ich möchte mehr über die produktkategorien von bugland ltd. wissen.', 'product_info'),
    ('habt ihr umweltfreundliche produkte bei bugland ltd.?', 'product_info'),
    ('welche produktlinien bietet bugland ltd. an?', 'product_info'),
    ('ich habe gehört, dass bugland ltd. neue produkte hat. was sind sie?', 'product_info'),
    ('könnte ich eine katalog von bugland ltd. produkten bekommen?', 'product_info'),
    ('gibt es produkte von bugland ltd. für spezielle anwendungen?', 'product_info'),
    ('ich bin neugierig auf die produkte von bugland ltd.', 'product_info'),
    ('kannst du mir die produktdetails von bugland ltd. geben?', 'product_info'),
    ('ich möchte die produkte von bugland ltd. vergleichen.', 'product_info'),
    ('habt ihr produkte von bugland ltd. für den außenbereich?', 'product_info'),
    ('was sind die preise für die produkte von bugland ltd.?', 'product_info'),
    ('gibt es produkte von bugland ltd. für haustiere?', 'product_info'),
    ('ich suche nach technischen produkten von bugland ltd.', 'product_info'),
    ('was sind die vorteile der produkte von bugland ltd.?', 'product_info'),
    ('ich möchte wissen, ob bugland ltd. gesunde produkte anbietet.', 'product_info'),
    ('was sind die häufigsten fragen zu den produkten von bugland ltd.?', 'product_info'),
    ('kannst du mir die produktverfügbarkeit von bugland ltd. mitteilen?', 'product_info'),

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

    # Troubleshooting
    ('was soll ich tun, wenn mein gerät nicht funktioniert?', 'troubleshooting'),
    ('wie kann ich probleme mit meinem gerät beheben?', 'troubleshooting'),
    ('was sind die ersten schritte zur fehlerbehebung?', 'troubleshooting'),
    ('mein gerät reagiert nicht. was kann ich tun?', 'troubleshooting'),
    ('gibt es eine anleitung zur fehlerbehebung für mein gerät?', 'troubleshooting'),
    ('wie finde ich heraus, warum mein gerät nicht funktioniert?', 'troubleshooting'),
    ('was kann ich tun, wenn mein gerät nicht startet?', 'troubleshooting'),
    ('gibt es tipps zur problemlösung für mein gerät?', 'troubleshooting'),
    ('wie kann ich häufige probleme mit meinem gerät lösen?', 'troubleshooting'),
    ('was mache ich, wenn mein gerät einen fehler anzeigt?', 'troubleshooting'),
    ('wie kann ich technische probleme mit meinem gerät beheben?', 'troubleshooting'),
    ('was sind die häufigsten probleme mit diesem gerät?', 'troubleshooting'),
    ('gibt es eine checklist für die fehlerbehebung?', 'troubleshooting'),
    ('wie kann ich mein gerät zurücksetzen?', 'troubleshooting'),
    ('was soll ich tun, wenn mein gerät überhitzt?', 'troubleshooting'),
    ('wie kann ich die leistung meines geräts verbessern?', 'troubleshooting'),
    ('gibt es spezielle anweisungen zur fehlerbehebung für mein gerät?', 'troubleshooting'),
    ('wie kann ich herausfinden, ob mein gerät defekt ist?', 'troubleshooting'),
    ('was kann ich tun, wenn mein gerät keine verbindung herstellt?', 'troubleshooting'),
    ('wie lange dauert es, ein problem mit meinem gerät zu beheben?', 'troubleshooting'),
    ('wer kann mir bei der fehlerbehebung helfen?', 'troubleshooting'),

    # Spare Parts
    ('wo kann ich ersatzteile für mein gerät finden?', 'spare_parts'),
    ('gibt es einen speziellen shop für ersatzteile?', 'spare_parts'),
    ('wo kaufe ich am besten ersatzteile?', 'spare_parts'),
    ('kannst du mir sagen, wo ich ersatzteile bekommen kann?', 'spare_parts'),
    ('gibt es eine website, die ersatzteile verkauft?', 'spare_parts'),
    ('wo finde ich originale ersatzteile für mein produkt?', 'spare_parts'),
    ('gibt es anbieter, die ersatzteile für mein gerät führen?', 'spare_parts'),
    ('wie finde ich die richtigen ersatzteile für mein gerät?', 'spare_parts'),
    ('wo kann ich günstige ersatzteile kaufen?', 'spare_parts'),
    ('gibt es einen katalog für ersatzteile?', 'spare_parts'),
    ('wo kann ich nach ersatzteilen suchen?', 'spare_parts'),
    ('wie kann ich sicherstellen, dass ich die richtigen ersatzteile bekomme?', 'spare_parts'),
    ('gibt es eine hotline für ersatzteilanfragen?', 'spare_parts'),
    ('wo finde ich eine liste von verfügbaren ersatzteilen?', 'spare_parts'),
    ('kann ich ersatzteile direkt beim hersteller kaufen?', 'spare_parts'),
    ('gibt es lokale geschäfte, die ersatzteile führen?', 'spare_parts'),
    ('wo kann ich nach gebrauchten ersatzteilen suchen?', 'spare_parts'),
    ('wie lange dauert es, ersatzteile zu bestellen?', 'spare_parts'),
    ('was muss ich beachten, wenn ich ersatzteile kaufe?', 'spare_parts'),
    ('gibt es spezielle websites für rare ersatzteile?', 'spare_parts'),

    # Repair Request
    ('was benötige ich, um eine reparatur anzufragen?', 'repair_request'),
    ('wie stelle ich eine reparaturanfrage?', 'repair_request'),
    ('was muss ich tun, um mein produkt reparieren zu lassen?', 'repair_request'),
    ('welche informationen werden für eine reparatur benötigt?', 'repair_request'),
    ('brauche ich einen nachweis für die reparaturanfrage?', 'repair_request'),
    ('was sind die schritte, um eine reparatur anzufordern?', 'repair_request'),
    ('kannst du mir sagen, was ich für eine reparatur brauche?', 'repair_request'),
    ('wie kann ich eine reparatur für mein gerät anfordern?', 'repair_request'),
    ('was sind die voraussetzungen für eine reparaturanfrage?', 'repair_request'),
    ('welche dokumente muss ich einreichen, um eine reparatur zu beantragen?', 'repair_request'),
    ('gibt es spezielle formulare für die reparaturanfrage?', 'repair_request'),
    ('wie lange dauert es, eine reparatur anzufordern?', 'repair_request'),
    ('muss ich mein produkt einschicken, um eine reparatur zu beantragen?', 'repair_request'),
    ('wo kann ich meine reparaturanfrage einreichen?', 'repair_request'),
    ('was sind die häufigsten anfragen für reparaturen?', 'repair_request'),
    ('wie kann ich den status meiner reparaturanfrage überprüfen?', 'repair_request'),
    ('kann ich die reparatur online anfordern?', 'repair_request'),
    ('was passiert, nachdem ich die reparaturanfrage gestellt habe?', 'repair_request'),
    ('wer kann mir bei der reparaturanfrage helfen?', 'repair_request'),
    ('gibt es gebühren für die reparaturanfrage?', 'repair_request'),
    ('was muss ich beachten, bevor ich eine reparatur anfrage?', 'repair_request'),

    # Warranty Info
    ('wie sieht es mit der garantie aus?', 'warranty_info'),
    ('was deckt die garantie ab?', 'warranty_info'),
    ('wie lange gilt die garantie für mein produkt?', 'warranty_info'),
    ('was muss ich tun, um die garantie in anspruch zu nehmen?', 'warranty_info'),
    ('gibt es eine garantie auf dieses produkt?', 'warranty_info'),
    ('was sind die garantiebedingungen?', 'warranty_info'),
    ('wie kann ich meine garantie überprüfen?', 'warranty_info'),
    ('gibt es eine erweiterte garantie?', 'warranty_info'),
    ('was passiert, wenn mein produkt während der garantie kaputt geht?', 'warranty_info'),
    ('kann ich die garantie verlängern?', 'warranty_info'),
    ('wie mache ich einen garantieanspruch geltend?', 'warranty_info'),
    ('was ist nicht durch die garantie abgedeckt?', 'warranty_info'),
    ('wie erfahre ich mehr über die garantie meines produkts?', 'warranty_info'),
    ('gibt es eine garantie auf gebrauchte produkte?', 'warranty_info'),
    ('wie lange habe ich zeit, um einen garantieanspruch zu stellen?', 'warranty_info'),
    ('wer ist mein ansprechpartner für garantiefragen?', 'warranty_info'),
    ('was sind die häufigsten fragen zur garantie?', 'warranty_info'),
    ('wie kann ich einen garantiefall melden?', 'warranty_info'),
    ('gibt es spezielle garantieangebote für bestimmte produkte?', 'warranty_info'),
    ('wie wird die garantie bei internationalen bestellungen gehandhabt?', 'warranty_info'),
    ('was muss ich bei der garantie beachten?', 'warranty_info'),

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
    ('ich hatte ein problem beim bezahlen.', 'customer_feedback'),

    # Order Problem     
    ('ich habe ein problem mit meiner bestellung.', 'order_problem'),
    ('meine bestellung ist noch nicht angekommen.', 'order_problem'),
    ('was kann ich tun, wenn meine bestellung verspätet ist?', 'order_problem'),
    ('ich habe die falsche bestellung erhalten.', 'order_problem'),
    ('wie kann ich den status meiner bestellung überprüfen?', 'order_problem'),
    ('was mache ich, wenn meine bestellung verloren gegangen ist?', 'order_problem'),
    ('ich möchte meine bestellung stornieren.', 'order_problem'),
    ('gibt es ein problem mit meiner bestellung?', 'order_problem'),
    ('wie lange dauert es, bis ich meine bestellung erhalte?', 'order_problem'),
    ('ich habe keine bestellbestätigung erhalten.', 'order_problem'),
    ('wie kann ich eine reklamation für meine bestellung einreichen?', 'order_problem'),
    ('ich möchte wissen, warum meine bestellung verzögert wird.', 'order_problem'),
    ('was sind die häufigsten probleme mit bestellungen?', 'order_problem'),
    ('wie kann ich meine lieferadresse für eine bestehende bestellung ändern?', 'order_problem'),
    ('ich habe ein problem mit der zahlung meiner bestellung.', 'order_problem'),
    ('kann ich meine bestellung nachträglich ändern?', 'order_problem'),
    ('ich habe ein defektes produkt in meiner bestellung erhalten.', 'order_problem'),
    ('wie kann ich den kundenservice zu meiner bestellung kontaktieren?', 'order_problem'),
    ('wo finde ich informationen zu meiner bestellung?', 'order_problem'),
    ('gibt es eine möglichkeit, meine bestellung zu verfolgen?', 'order_problem'),
    ('ich habe versehentlich die falsche menge bestellt.', 'order_problem'),

    # Payment Issue
    ('ich habe ein problem mit meiner zahlung.', 'payment_issue'),
    ('meine zahlung wurde nicht akzeptiert.', 'payment_issue'),
    ('was kann ich tun, wenn meine kreditkarte abgelehnt wurde?', 'payment_issue'),
    ('ich habe keine bestätigung für meine zahlung erhalten.', 'payment_issue'),
    ('wie kann ich meine zahlung überprüfen?', 'payment_issue'),
    ('gibt es ein problem mit meiner rechnung?', 'payment_issue'),
    ('ich möchte meine zahlungsart ändern.', 'payment_issue'),
    ('warum wurde meine zahlung zurückgebucht?', 'payment_issue'),
    ('wie lange dauert es, bis meine zahlung bearbeitet wird?', 'payment_issue'),
    ('ich habe versehentlich zu viel bezahlt.', 'payment_issue'),
    ('wie kann ich eine erstattung für meine zahlung beantragen?', 'payment_issue'),
    ('ich habe ein problem mit der zahlung für meine bestellung.', 'payment_issue'),
    ('wie kann ich meine zahlung stornieren?', 'payment_issue'),
    ('ich habe ein problem mit der zahlungsbestätigung.', 'payment_issue'),
    ('kann ich meine zahlung nachträglich ändern?', 'payment_issue'),
    ('was mache ich, wenn ich eine fehlerhafte zahlung getätigt habe?', 'payment_issue'),
    ('wie kann ich den kundenservice bei zahlungsproblemen kontaktieren?', 'payment_issue'),
    ('gibt es zusätzliche gebühren für meine zahlung?', 'payment_issue'),
    ('ich möchte wissen, ob meine zahlung erfolgreich war.', 'payment_issue'),
    ('warum wird meine zahlung nicht verarbeitet?', 'payment_issue'),

    # Security Concerns
    ('sind die produkte von bugland ltd. sicher zu verwenden?', 'security_concerns'),
    ('gibt es bekannte sicherheitsprobleme mit den produkten von bugland ltd.?', 'security_concerns'),
    ('wie schützt bugland ltd. meine daten bei der nutzung ihrer produkte?', 'security_concerns'),
    ('was unternimmt bugland ltd. gegen sicherheitsrisiken?', 'security_concerns'),
    ('sind die produkte von bugland ltd. gegen hacking geschützt?', 'security_concerns'),
    ('gibt es sicherheitszertifikate für die produkte von bugland ltd.?', 'security_concerns'),
    ('wie kann ich sicherstellen, dass die produkte von bugland ltd. sicher sind?', 'security_concerns'),
    ('was sagt bugland ltd. über die sicherheit ihrer produkte?', 'security_concerns'),
    ('wie geht bugland ltd. mit sicherheitsvorfällen um?', 'security_concerns'),
    ('sind die produkte von bugland ltd. nach internationalen sicherheitsstandards zertifiziert?', 'security_concerns'),
    ('kann ich sicher sein, dass meine informationen bei bugland ltd. geschützt sind?', 'security_concerns'),
    ('wie oft überprüft bugland ltd. die sicherheit ihrer produkte?', 'security_concerns'),
    ('was soll ich tun, wenn ich sicherheitsbedenken bezüglich eines produkts von bugland ltd. habe?', 'security_concerns'),
    ('gibt es eine hotline für sicherheitsfragen zu bugland ltd. produkten?', 'security_concerns'),
    ('wie informiert bugland ltd. über sicherheitsupdates?', 'security_concerns'),
    ('sind die produkte von bugland ltd. gegen malware geschützt?', 'security_concerns'),
    ('was sind die sicherheitsfunktionen der produkte von bugland ltd.?', 'security_concerns'),
    ('wie kann ich bugland ltd. kontaktieren, wenn ich sicherheitsbedenken habe?', 'security_concerns'),
    ('gibt es sicherheitswarnungen für bestimmte produkte von bugland ltd.?', 'security_concerns'),
    ('was macht bugland ltd. um die sicherheit ihrer kunden zu gewährleisten?', 'security_concerns'),
    ('sind die produkte sicher zu verwenden?', 'security_concerns'),
    ('gibt es bekannte sicherheitsprobleme mit den produkten?', 'security_concerns'),
    ('wie schützt das unternehmen meine daten bei der nutzung ihrer produkte?', 'security_concerns'),
    ('was unternimmt das unternehmen gegen sicherheitsrisiken?', 'security_concerns'),
    ('sind die produkte gegen hacking geschützt?', 'security_concerns'),
    ('gibt es sicherheitszertifikate für die produkte?', 'security_concerns'),
    ('wie kann ich sicherstellen, dass die produkte sicher sind?', 'security_concerns'),
    ('was sagt das unternehmen über die sicherheit seiner produkte?', 'security_concerns'),
    ('wie geht das unternehmen mit sicherheitsvorfällen um?', 'security_concerns'),
    ('sind die produkte nach internationalen sicherheitsstandards zertifiziert?', 'security_concerns'),
    ('kann ich sicher sein, dass meine informationen geschützt sind?', 'security_concerns'),
    ('wie oft überprüft das unternehmen die sicherheit seiner produkte?', 'security_concerns'),
    ('was soll ich tun, wenn ich sicherheitsbedenken bezüglich eines produkts habe?', 'security_concerns'),
    ('gibt es eine hotline für sicherheitsfragen zu den produkten?', 'security_concerns'),
    ('wie informiert das unternehmen über sicherheitsupdates?', 'security_concerns'),
    ('sind die produkte gegen malware geschützt?', 'security_concerns'),
    ('was sind die sicherheitsfunktionen der produkte?', 'security_concerns'),
    ('wie kann ich das unternehmen kontaktieren, wenn ich sicherheitsbedenken habe?', 'security_concerns'),
    ('gibt es sicherheitswarnungen für bestimmte produkte?', 'security_concerns'),
    ('was macht das unternehmen, um die sicherheit seiner kunden zu gewährleisten?', 'security_concerns'),

    # Ultimate Answer
    ('was ist die ultimative antwort auf das leben, das universum und alles?', 'ultimate_answer'),
    ('kannst du mir die ultimative antwort geben?', 'ultimate_answer'),
    ('was ist die bedeutung des lebens?', 'ultimate_answer'),
    ('gibt es eine einfache antwort auf alles?', 'ultimate_answer'),
    ('was ist die antwort auf die ultimative frage?', 'ultimate_answer'),
    ('was ist die essenz des lebens?', 'ultimate_answer'),
    ('kannst du mir die geheimnisse des universums verraten?', 'ultimate_answer'),
    ('was ist die wichtigste frage, die man stellen kann?', 'ultimate_answer'),
    ('was ist die ultimative wahrheit?', 'ultimate_answer'),
    ('gibt es eine universelle antwort auf alle fragen?', 'ultimate_answer'),
    ('was ist der sinn des lebens?', 'ultimate_answer'),
    ('was ist die zentrale frage des existenz?', 'ultimate_answer'),
    ('was ist der schlüssel zum universum?', 'ultimate_answer'),
    ('was ist die ultimative erkenntnis?', 'ultimate_answer'),
    ('was ist das größte geheimnis des lebens?', 'ultimate_answer'),
    ('was ist die bedeutung des seins?', 'ultimate_answer'),
    ('kannst du mir die antwort auf die große frage geben?', 'ultimate_answer'),
    ('was ist die ultimative philosophie?', 'ultimate_answer'),
    ('was ist der grund für unsere existenz?', 'ultimate_answer'),
    ('was ist die ultimative lösung?', 'ultimate_answer'),
    ('was ist die wichtigste antwort, die ich wissen sollte?', 'ultimate_answer'),

    # Best Programmers
    ('wer sind die besten programmierer aller zeiten?', 'best_programmers'),
    ('kannst du mir sagen, wer die top programmierer sind?', 'best_programmers'),
    ('wer gilt als der beste programmierer?', 'best_programmers'),
    ('wer sind die berühmtesten programmierer?', 'best_programmers'),
    ('wer hat die meisten einflüsse auf die programmierung gehabt?', 'best_programmers'),
    ('kannst du mir die besten programmierer nennen?', 'best_programmers'),
    ('wer sind die legendären programmierer in der geschichte?', 'best_programmers'),
    ('wer hat die besten beiträge zur softwareentwicklung geleistet?', 'best_programmers'),
    ('wer sind die innovativsten programmierer?', 'best_programmers'),
    ('wer hat die besten programmiersprachen entwickelt?', 'best_programmers'),
    ('wer sind die einflussreichsten programmierer in der technologie?', 'best_programmers'),
    ('kannst du mir die besten programmierer im 21. jahrhundert nennen?', 'best_programmers'),
    ('wer sind die bekanntesten weiblichen programmierer?', 'best_programmers'),
    ('wer hat die meisten bedeutenden projekte geleitet?', 'best_programmers'),
    ('wer sind die besten programmierer in der open-source-community?', 'best_programmers'),
    ('wer sind die besten programmierer in der geschichte der computerwissenschaft?', 'best_programmers'),
    ('wer hat die größten innovationen in der programmierung hervorgebracht?', 'best_programmers'),
    ('wer sind die besten programmierer in der gaming-industrie?', 'best_programmers'),
    ('wer sind die besten programmierer in der webentwicklung?', 'best_programmers'),
    ('wer sind die besten programmierer in der künstlichen intelligenz?', 'best_programmers'),
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
        "Tschüss!",
        "Mein CleanBug macht seltsame Geräusche",
        "Wie kann ich eine Rückgabe veranlassen?",
        "Wer sind die besten Programmierer?"
    ]

    for text in test_texts:
        intent = recognizer.predict_intent(text)
        print(f"Text: {text} -> Absicht: {intent}")