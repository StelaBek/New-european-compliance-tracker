"""Official feed/API ingestion; errors are visible, never silently count as success."""
import requests
import feedparser
from urllib.parse import urljoin
from core import make_record, official_url

HEADERS={'User-Agent':'EuropeanProductComplianceResearch/0.1 (public regulatory metadata collection)'}

def _get(url, domain):
    if not official_url(url,domain): raise ValueError('Source URL outside registered official domain')
    r=requests.get(url,headers=HEADERS,timeout=25,allow_redirects=False)
    hops=0
    while r.status_code in (301,302,303,307,308) and hops<4:
        new=urljoin(r.url,r.headers.get('Location',''))
        if not official_url(new,domain): raise ValueError('Source redirect leaves registered official domain')
        r=requests.get(new,headers=HEADERS,timeout=25,allow_redirects=False); hops+=1
    r.raise_for_status()
    if len(r.content)>6_000_000: raise ValueError('Source response too large')
    return r

def _feed_items(source, content):
    feed=feedparser.parse(content)
    if feed.bozo and not feed.entries: raise ValueError('Invalid RSS/Atom XML')
    rows=[]
    for e in feed.entries[:100]:
        url=e.get('link','')
        rows.append({'title':e.get('title',''), 'document_url':url,
                     'published_at':e.get('published',e.get('updated','')),
                     'excerpt':e.get('summary','')})
    return rows

def _riksdagen_items(payload):
    root=payload.get('dokumentlista',{})
    docs=root.get('dokument',[])
    if isinstance(docs,dict): docs=[docs]
    result=[]
    for d in docs:
        url=d.get('dokument_url_html') or d.get('dokument_url_text') or d.get('url') or ''
        result.append({'title':d.get('titel',''), 'document_url':url,
                       'published_at':d.get('datum',''), 'excerpt':d.get('undertitel','') or ''})
    return result

def scan_source(source):
    try:
        r=_get(source['url'],source['domain'])
        if source['kind']=='feed': items=_feed_items(source,r.content)
        elif source['kind']=='riksdagen': items=_riksdagen_items(r.json())
        else: raise ValueError('Unsupported adapter')
        records=[row for i in items if (row:=make_record(source,i))]
        if not items: raise ValueError('Endpoint returned no items')
        return records, {'ok':True,'raw_items':len(items),'accepted_documents':len(records),
                         'error':'','source_url':source['url']}
    except (requests.RequestException, ValueError, KeyError, TypeError) as e:
        return [],{'ok':False,'raw_items':0,'accepted_documents':0,
                   'error':f'{type(e).__name__}: {str(e)[:240]}','source_url':source['url']}
