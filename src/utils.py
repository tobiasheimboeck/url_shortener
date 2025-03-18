import string
import random
from models import db, ShortUrl, ShortUrlAnalytics


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def cleanup_expired_urls():
    expired_urls = ShortUrl.query.filter(ShortUrl.is_expired).all()

    for url in expired_urls:
        db.session.delete(url)

    db.session.commit()