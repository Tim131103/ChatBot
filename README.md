# Chatbot-Projekt

Dieses Projekt zielt darauf ab, einen Chatbot zu entwickeln, der mit Hilfe von objektorientierter Programmierung (OOP) und Vererbung in Python erstellt wird. Der Chatbot soll in der Lage sein, Benutzeranfragen zu verstehen und entsprechend zu antworten. Wir arbeiten zu dritt an diesem Projekt in Visual Studio Code.

## Projektstruktur

### Hauptkomponenten

1. **Logik des Bots:**
   - Verwendung von Klassen und Objekten zur Strukturierung der Bot-Logik.
   - Implementierung von Vererbung zur Erstellung spezialisierter Bot-Varianten.

2. **Design/Interface:**
   - Entwicklung einer Benutzeroberfläche mit Tkinter, PyQt oder einer Weboberfläche mit Flask/Django.
   - Sicherstellung einer intuitiven Benutzerführung.

3. **Verarbeitung der Daten:**
   - Implementierung der Intent-Erkennung mit Bibliotheken wie NLTK oder spaCy.
   - Verwaltung von Utterances/Variances zur Erkennung unterschiedlicher Ausdrucksweisen für denselben Intent.

4. **Entscheidungsbaum:**
   - Nutzung von Entscheidungsbäumen zur Modellierung der Bot-Logik mit scikit-learn.
   - Unterstützung beim Debugging und der Entwicklung durch visuelle Darstellung der Logik.

5. **Datenbankintegration:**
   - Speicherung von Chatverläufen in SQL-Datenbanken wie SQLite oder PostgreSQL.
   - Entwurf von Datenbanktabellen für Benutzer, Intents und Chatverläufe.

6. **Teststrategie:**
   - Implementierung von Unit-Tests und Integrationstests zur Überprüfung der Logik.
   - Entwicklung einer Teststrategie zur Qualitätssicherung.

### Weitere Überlegungen

- **AI-API-Integration:** Integration von AI-APIs wie Google Dialogflow oder IBM Watson zur Verbesserung der Intent-Erkennung.
- **Service Line und Support:** Implementierung einer Eskalationslogik zur Weiterleitung von Anfragen an menschliche Mitarbeiter.
- **Automatisierte E-Mails:** Funktion zur automatischen Versendung von E-Mails bei Bedarf.

## Verwendete Bibliotheken

- **NLP:** NLTK, spaCy, TextBlob
- **Machine Learning:** scikit-learn, TensorFlow, PyTorch
- **Datenbank:** SQLAlchemy, SQLite3
- **Web-Frameworks:** Flask, Django
- **API-Integration:** Requests, Flask-RESTful
- **Testing:** unittest, pytest
- **Logging und Debugging:** logging, pdb

## Installation

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/Tim131103/chatbot-projekt.git

   cd chatbot-projekt

   pip install -r requirements.txt

   python main.py

## Mitwirkende

- [Tim](https://github.com/Tim131103) 
- [Lykka](https://github.com/Lykka2)
- [Jean-Luc](https://github.com/jean-lucleminskz7478)

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der Datei `LICENSE`.
