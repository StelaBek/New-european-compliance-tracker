"""Deterministic JSON snapshots committed by GitHub Actions for Streamlit Cloud."""
import json
import os
from pathlib import Path
from core import utcnow

DATA=Path(os.getenv('COMPLIANCE_DATA_DIR',str(Path(__file__).parent/'data')))
SNAPSHOT=DATA/'snapshot.json'

def empty(): return {'generated_at':'','records':[],'health':{},'reviews':{}}

def load():
    if not SNAPSHOT.exists(): return empty()
    try:
        data=json.loads(SNAPSHOT.read_text(encoding='utf-8'))
        if not isinstance(data,dict): return empty()
        return {**empty(),**data}
    except (json.JSONDecodeError,OSError): return empty()

def save(data):
    DATA.mkdir(parents=True,exist_ok=True)
    tmp=SNAPSHOT.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(SNAPSHOT)

def merge_scan(before,results,health):
    old={x['id']:x for x in before['records']}
    for record in results:
        if record['id'] in old:
            record['reviewer']=old[record['id']].get('reviewer','')
            record['reviewed_at']=old[record['id']].get('reviewed_at','')
            record['verification']=old[record['id']].get('verification','unreviewed')
            record['assessment']=old[record['id']].get('assessment',record['assessment'])
        old[record['id']]=record
    return {'generated_at':utcnow(),'records':list(old.values()),
            'health':{**before['health'],**health}, 'reviews':before.get('reviews',{})}
