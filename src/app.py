from flask import Flask

from models import db
from routes import shorten_url, redirect_to_original_url

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.add_url_rule("/shorten", "shorten_url", shorten_url, methods=["POST"])
app.add_url_rule("/<short_code>", "redirect_to_original_url", redirect_to_original_url)

if __name__ == "__main__":
    app.run(debug=True)
