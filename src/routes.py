import validators
from flask import request, jsonify, redirect
from models import db, ShortUrl, ShortUrlAnalytics
from utils import generate_short_code
from datetime import datetime, timedelta


@db.event.listens_for(db.session, 'after_flush')
def create_analytics_entry(session, flush_context):
    for short_url in session.new:
        if isinstance(short_url, ShortUrl):
            analytics_entry = ShortUrlAnalytics(short_code=short_url.short_code)
            session.add(analytics_entry)

def shorten_url():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    if not validators.url(original_url):
        return jsonify({"error": "Invalid URL format."}), 400

    short_code = generate_short_code()

    while ShortUrl.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    expires_at = datetime.now() + timedelta(seconds=20)

    new_url = ShortUrl(short_code=short_code, original_url=original_url, expires_at=expires_at)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({"short_url": f"http://localhost:5000/{short_code}"})


def redirect_to_original_url(short_code):
    url_entry: ShortUrl = ShortUrl.query.filter_by(short_code=short_code).first()

    if not url_entry:
        return jsonify({"error": "Short URL not found"}), 404

    if url_entry.is_expired():
        db.session.delete(url_entry)
        db.session.commit()
        return jsonify({"error": "Short URL has expired"}), 410

    url_analytics_entry = ShortUrlAnalytics.query.filter_by(short_code=short_code).first()
    url_analytics_entry.visits += 1
    db.session.commit()

    return redirect(url_entry.original_url)
