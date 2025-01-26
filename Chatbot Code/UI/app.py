from flask import Flask, render_template

app = Flask(__name__, 
            template_folder='../Chatbot Code/templates',
            static_folder='../Chatbot Code/static')

@app.route('/')
def home():
    return render_template('chatbot_ui.html')

if __name__ == "__main__":
    app.run(debug=True)
