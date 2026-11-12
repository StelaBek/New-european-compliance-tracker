"""Coverage registry for Europe. Listing a country never implies data coverage."""
from taxonomy import COUNTRIES, STARTER_SOURCES
from official_sources import DIRECTORY

# Initial adapters use exact official feed/API endpoints. Endpoint health is tested at runtime.
# Integration adapters for other countries must be added only after endpoint validation.
SOURCES = [
    {'id':'eu-oj', 'country':'European Union', 'name':'EUR-Lex Official Journal RSS',
     'kind':'feed', 'url':'https://eur-lex.europa.eu/EN/display-feed.rss?rssId=165',
     'domain':'eur-lex.europa.eu', 'scope':'Selected Official Journal notifications', 'enabled':True},
    {'id':'uk-new', 'country':'United Kingdom', 'name':'UK legislation Atom feed',
     'kind':'feed', 'url':'https://www.legislation.gov.uk/new/data.feed',
     'domain':'legislation.gov.uk', 'scope':'Recently published UK legislation', 'enabled':True},
    {'id':'de-feed', 'country':'Germany', 'name':'Gesetze im Internet updates RSS',
     'kind':'feed', 'url':'https://www.gesetze-im-internet.de/aktuDienst-rss-feed.xml',
     'domain':'gesetze-im-internet.de', 'scope':'Selected federal legislation updates', 'enabled':True},
    {'id':'no-feed', 'country':'Norway', 'name':'Lovdata announcements RSS',
     'kind':'feed', 'url':'https://lovdata.no/feed?data=LT&type=RSS',
     'domain':'lovdata.no', 'scope':'Selected national publication notifications', 'enabled':True},
    {'id':'se-api', 'country':'Sweden', 'name':'Riksdagen documents JSON API',
     'kind':'riksdagen', 'url':'https://data.riksdagen.se/dokumentlista/?utformat=json&sort=datum&sortorder=desc&sz=50',
     'domain':'data.riksdagen.se', 'scope':'Parliamentary document list (not full enacted-law archive)', 'enabled':True},
]

def country_matrix(health):
    out=[]
    for country in COUNTRIES:
        active=[s for s in SOURCES if s['country']==country and s['enabled']]
        successful=[s for s in active if health.get(s['id'],{}).get('ok')]
        out.append({'country':country, 'sources_configured':len(active),
                    'sources_successful':len(successful), 'status':
                    'Partial source monitored' if successful else
                    'Configured; scan not validated' if active else 'No ingestion connector',
                    'full_coverage_verified':False})
    return out

def portals(country):
    return [d for d in DIRECTORY if d['country']==country and d['connector']=='portal']
