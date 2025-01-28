import nltk
import joblib 

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class IntentRecognizer:
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer
        self.stop_words = set(stopwords.words('german'))
        
    def preprocess_text(self,text):
        """
        Preprocessing the input text:
        - tokenize
        - removing of so called stopwords (i.e. 'und', 'aber', etc.)
        - lemmatize (transform words to their base form)
        """
        tokens = word_tokenize(text.lower)
        tokens = [word for word in tokens if word not in self.stop_words]
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

    def predict_intent(self, text):
        if self.model is None:
            raise ValueError("Das Modell wurde noch nicht trainiert.")
        processed_text = self.preprocess_text(text)
        return self.model.predict([processed_text])[0]
    
#TODO: Create Training Data
training_data = [
    ("text", "intent")
]

if __name__ == "__main__":
    recognizer = IntentRecognizer()

    recognizer.train(training_data)

    #TODO: Ersetzen mit Tests von Lykka
    test_texts = [
        "hi",
        "Kannst du mir Infos zur Windowfly geben?",
        "Tschüss!"
    ]

    for text in test_texts:
        intent = recognizer.predict_intent(text)
        print(f"Text: {text} -> Absicht: {intent}")