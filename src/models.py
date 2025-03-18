from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone

db = SQLAlchemy()

class ShortUrl(db.Model):
    short_code = db.Column(db.String(6), primary_key=True, unique=True, nullable=False)
    original_url = db.Column(db.String(2048), nullable=False)
    analytics = db.relationship("ShortUrlAnalytics", backref="short_url", uselist=False)
    expires_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc) + timedelta(days=2))

    def is_expired(self):
        return self.expires_at < datetime.now()

class ShortUrlAnalytics(db.Model):
    short_code = db.Column(db.String(6), db.ForeignKey('short_url.short_code'), primary_key=True, unique=True, nullable=False)
    clicked_times = db.Column(db.Integer, default=0, nullable=False)
