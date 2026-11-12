"""Conservative regulatory evidence model: source collection is not legal approval."""
from __future__ import annotations
import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urlsplit
from taxonomy import CATEGORIES, TOPICS

REQUIRED = ('source_id', 'jurisdiction', 'title', 'document_url')

def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def official_url(url: str, domain: str) -> bool:
    try:
        p = urlsplit(url)
        host = (p.hostname or '').lower().rstrip('.')
        domain = domain.lower().strip().rstrip('.')
        return (p.scheme == 'https' and not p.username and not p.password and
                bool(host) and bool(domain) and (host == domain or host.endswith('.'+domain)) and
                not host.replace('.', '').isdigit())
    except (TypeError, ValueError):
        return False

def document_url(url: str, domain: str) -> bool:
    return official_url(url, domain) and urlsplit(url).path.strip('/') not in ('', 'en', 'home', 'index.html')

def categories_for(text: str):
    hay = (text or '').casefold()
    return [category for category, terms in CATEGORIES.items() if terms and
            any(re.search(r'(?<!\w)' + re.escape(term.casefold()) + r'(?!\w)', hay) for term in terms)]

def topics_for(text: str):
    hay = (text or '').casefold()
    return [topic for topic, terms in TOPICS.items() if any(t.casefold() in hay for t in terms)]

def make_record(source, item):
    title = (item.get('title') or '').strip()[:500]
    url = (item.get('document_url') or '').strip()
    if not title or not document_url(url, source['domain']):
        return None
    body = (item.get('excerpt') or '').strip()[:3000]
    context = f'{title} {body}'
    categories = categories_for(context)
    identifier = hashlib.sha256((source['id'] + '|' + url).encode()).hexdigest()[:20]
    return {'id':identifier, 'source_id':source['id'], 'jurisdiction':source['country'],
            'title':title, 'document_url':url, 'published_at':item.get('published_at',''),
            'retrieved_at':utcnow(), 'excerpt':body, 'categories':categories,
            'topics':topics_for(context), 'relevance':'candidate' if categories else 'not_classified',
            'verification':'unreviewed', 'legal_change':'not_determined',
            'assessment':'Source metadata only. Exact changes and legal obligations have not been verified.',
            'reviewer':'', 'reviewed_at':'', 'source_type':source['kind']}

def safe_summary(record):
    return f"Publication candidate from {record['jurisdiction']}. Title: {record['title']}. " \
           'Changes, affected products, legal dates and required actions require examination of the official act.'
