from flask import Flask, render_template

# Initialize the Flask application with the correct paths for templates and static files
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

@app.route('/')
def home():
    """Render the chatbot UI."""
    return render_template('chatbot_ui.html')

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)