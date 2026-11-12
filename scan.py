"""CLI entrypoint for daily Github Actions and local execution."""
from core import utcnow
from ingestion import scan_source
from source_registry import SOURCES
from storage import load,save,merge_scan

def run():
    before=load(); records=[]; health={}
    for source in SOURCES:
        if not source['enabled']:continue
        items, report=scan_source(source)
        health[source['id']]={**report,'checked_at':utcnow()}
        print(f"{source['country']}: {len(items)} documents; {'OK' if report['ok'] else report['error']}")
        records.extend(items)
    merged=merge_scan(before,records,health)
    save(merged)
    print('Snapshot records:',len(merged['records']))
    return merged

if __name__=='__main__': run()
