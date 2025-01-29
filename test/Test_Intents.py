import nltk
import joblib
import unittest

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Ensure necessary NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class IntentRecognizer:
    def __init__(self, stop_words_language='german'):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words(stop_words_language))
        self.model = None

    def preprocess_text(self, text):
        """
        Preprocess the input text by tokenizing, removing stopwords, and lemmatizing.
        """
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return " ".join(tokens)

    def train(self, training_data):
        """
        Train the model with the given training data.
        """
        texts = [self.preprocess_text(text) for text, intent in training_data]
        intents = [intent for text, intent in training_data]

        self.model = make_pipeline(CountVectorizer(), MultinomialNB())
        self.model.fit(texts, intents)

    def predict_intent(self, text):
        """
        Predict the intent of the given text.
        """
        if self.model is None:
            raise ValueError("The model has not been trained yet.")
        processed_text = self.preprocess_text(text)
        return self.model.predict([processed_text])[0]

    def save_model(self, filename):
        """
        Save the trained model to a file.
        """
        if self.model is None:
            raise ValueError("There is no model to save.")
        joblib.dump(self.model, filename)
        print(f"Model saved to {filename}.")

    def load_model(self, filename):
        """
        Load a trained model from a file.
        """
        self.model = joblib.load(filename)

# Sample training data
training_data = [
    ("hallo", "greeting"),
    ("tschüss", "goodbye"),
    ("was kannst du für mich tun?", "help"),
    # Add more training data as needed
]

class TestIntentRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = IntentRecognizer()
        self.recognizer.train(training_data)

    def test_predict_intent(self):
        test_cases = [
            ("hallo", "greeting"),
            ("tschüss", "goodbye"),
            ("was kannst du für mich tun?", "help"),
        ]
        for text, expected_intent in test_cases:
            with self.subTest(text=text):
                self.assertEqual(self.recognizer.predict_intent(text), expected_intent)

    def test_model_save_and_load(self):
        filename = 'test_model.pkl'
        self.recognizer.save_model(filename)
        new_recognizer = IntentRecognizer()
        new_recognizer.load_model(filename)
        self.assertEqual(new_recognizer.predict_intent("hallo"), "greeting")

if __name__ == "__main__":
    unittest.main()