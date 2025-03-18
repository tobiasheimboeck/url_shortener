import string
import random
import validators
from flask import request, jsonify, redirect
from models import db, ShortUrl, ShortUrlAnalytics

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

# Event listener to create analytics entry after a new ShortUrl is created
@db.event.listens_for(db.session, 'after_flush')
def create_analytics_entry(session, flush_context):
    for short_url in session.new:
        if isinstance(short_url, ShortUrl):
            analytics_entry = ShortUrlAnalytics(short_code=short_url.short_code)
            session.add(analytics_entry)

# Event listener to delete analytics entry after ShortUrl deletion
@db.event.listens_for(ShortUrl, "after_delete")
def delete_analytics_entry(mapper, connection, target):
    analytics_entry = ShortUrlAnalytics.query.filter_by(short_code=target.short_code).first()
    db.session.delete(analytics_entry)
    db.session.commit()

def shorten_url():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "No URL provided"}), 400

    if not validators.url(original_url):
        return jsonify({"error": "Invalid URL format."}), 400

    short_code = generate_short_code()

    # Ensure unique short code
    while ShortUrl.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = ShortUrl(short_code=short_code, original_url=original_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({"short_url": f"http://localhost:5000/{short_code}"})

def redirect_to_original_url(short_code):
    url_entry = ShortUrl.query.filter_by(short_code=short_code).first()

    if url_entry:
        return redirect(url_entry.original_url)

    return jsonify({"error": "Short URL not found"}), 404