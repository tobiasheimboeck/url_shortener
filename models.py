from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ShortUrl(db.Model):
    short_code = db.Column(db.String(6), primary_key=True, unique=True, nullable=False)
    original_url = db.Column(db.String(2048), nullable=False)
    analytics = db.relationship("ShortUrlAnalytics", backref="short_url", uselist=False)

class ShortUrlAnalytics(db.Model):
    short_code = db.Column(db.String(6), db.ForeignKey('short_url.short_code'), primary_key=True, unique=True, nullable=False)
    clicked_times = db.Column(db.Integer, default=0, nullable=False)
