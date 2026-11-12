from core import official_url,document_url,make_record,categories_for
from source_registry import SOURCES,country_matrix

def test_reject_lookalike_domain():
    assert not official_url('https://legislation.gov.uk.attacker.example/act','legislation.gov.uk')
    assert official_url('https://www.legislation.gov.uk/ukpga/2026/1','legislation.gov.uk')

def test_reject_source_homepage():
    assert not document_url('https://legislation.gov.uk/','legislation.gov.uk')

def test_only_document_links():
    source=SOURCES[1]
    assert make_record(source,{'title':'Act 5','document_url':'https://example.com/foo'}) is None

def test_no_invented_law_change():
    source=SOURCES[1]
    r=make_record(source,{'title':'Furniture safety notice','document_url':'https://www.legislation.gov.uk/uksi/2026/999/contents'})
    assert r['verification']=='unreviewed'
    assert r['legal_change']=='not_determined'
    assert 'Furniture & upholstery' in r['categories']

def test_country_coverage_is_not_falsely_approved():
    rows=country_matrix({})
    assert len(rows)>=45
    assert all(not r['full_coverage_verified'] for r in rows)

def test_official_source_registry_only():
    assert all(official_url(s['url'],s['domain']) for s in SOURCES)
