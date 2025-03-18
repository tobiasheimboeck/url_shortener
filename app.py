from flask import Flask

from models import db
from routes import shorten_url, redirect_to_original_url

app = Flask(__name__)

# Load configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Register routes
app.add_url_rule("/shorten", "shorten_url", shorten_url, methods=["POST"])
app.add_url_rule("/<short_code>", "redirect_to_original_url", redirect_to_original_url)

if __name__ == "__main__":
    app.run(debug=True)
