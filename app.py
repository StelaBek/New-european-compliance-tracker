import json
import pandas as pd
import streamlit as st
from pathlib import Path
from taxonomy import COUNTRIES, CATEGORIES
from source_registry import SOURCES, country_matrix, portals
from storage import load
from core import safe_summary

st.set_page_config(page_title='European Product Compliance Intelligence', page_icon='⚖️',layout='wide')
st.markdown('''<style>.block-container{max-width:1320px;padding-top:1.8rem}.stMetric{border:1px solid #d9e0e5;border-radius:12px;padding:15px;background:#f8fafb}h1,h2,h3{letter-spacing:-.02em}</style>''',unsafe_allow_html=True)
data=load(); health=data['health']; records=data['records']; matrix=country_matrix(health)
st.title('European Product Compliance Intelligence')
st.caption('Official-source research dashboard • Source retrieval ≠ complete country coverage ≠ verified legal advice')
page=st.sidebar.radio('Navigate',['Overview','Document candidates','Country coverage','Official source registry','Review protocol'],index=0)
st.sidebar.info('No country is classified as fully monitored unless its publication register is comprehensively audited. AI does not approve laws or determine compliance.')

if page=='Overview':
    a,b,c,d=st.columns(4)
    a.metric('Jurisdictions listed',len(COUNTRIES))
    b.metric('Sources configured',sum(s['enabled'] for s in SOURCES))
    c.metric('Sources scanned successfully',sum(1 for s in SOURCES if health.get(s['id'],{}).get('ok')))
    d.metric('Document candidates',len(records))
    st.subheader('Coverage at a glance')
    st.warning('Complete country coverage: **not established**. A successful source scan only proves that particular endpoint responded and returned records.')
    st.dataframe(pd.DataFrame(matrix),use_container_width=True,hide_index=True)
    st.caption('Generated: '+(data['generated_at'] or 'No scheduled scan snapshot found. Run python scan.py or GitHub Actions.'))

elif page=='Document candidates':
    st.subheader('Candidate documents')
    st.write('These are source records, not confirmed amendments. Exact legal impact must be checked against the linked act and prior versions.')
    c1,c2,c3=st.columns(3)
    countries=sorted(set(r['jurisdiction'] for r in records))
    cc=c1.selectbox('Jurisdiction',['All']+countries)
    category=c2.selectbox('Product category',['All']+list(CATEGORIES))
    query=c3.text_input('Search title / excerpt')
    filtered=[r for r in records if (cc=='All' or r['jurisdiction']==cc) and
              (category=='All' or category in r['categories']) and
              (not query or query.casefold() in (r['title']+' '+r['excerpt']).casefold())]
    st.caption(f'{len(filtered)} document candidates')
    for r in sorted(filtered,key=lambda x:x.get('published_at',''),reverse=True)[:200]:
        with st.container(border=True):
            st.markdown('#### '+r['title'])
            st.caption(f"{r['jurisdiction']} · {r.get('published_at') or 'Date unavailable'} · Verification: {r['verification']} · Change status: {r['legal_change']}")
            if r['categories']:st.write('**Possible product categories:** '+', '.join(r['categories']))
            st.write(safe_summary(r))
            if r.get('excerpt'):st.caption('Publisher excerpt (not validated legal text): '+r['excerpt'][:450])
            st.link_button('Open exact publisher document',r['document_url'])
    st.download_button('Export candidates as JSON',json.dumps(filtered,ensure_ascii=False,indent=2),file_name='document_candidates.json',mime='application/json')

elif page=='Country coverage':
    st.subheader('Country-by-country monitoring audit')
    chosen=st.selectbox('Select country',COUNTRIES)
    row=next(x for x in matrix if x['country']==chosen)
    st.info(f"**{row['status']}** · {row['sources_configured']} connectors configured · {row['sources_successful']} passed the most recent fetch")
    st.write('**Full database coverage verified:** No. This requires a complete publication register, pagination/backfill, amendments, and reconciliation.')
    associated=[s for s in SOURCES if s['country']==chosen]
    for s in associated:
        h=health.get(s['id'],{})
        with st.container(border=True):
            st.write('**'+s['name']+'**')
            st.caption(s['scope'])
            st.write(f"Fetch status: {'Successful (partial)' if h.get('ok') else 'Not yet successful'}; documents accepted: {h.get('accepted_documents',0)}")
            if h.get('error'):st.error(h['error'])
            st.link_button('Official source endpoint',s['url'])
    for source in portals(chosen):
        st.link_button('Official publisher directory: '+source['name'],source['url'])
    st.dataframe(pd.DataFrame(matrix),hide_index=True,use_container_width=True)

elif page=='Official source registry':
    st.subheader('Direct source connectors')
    st.write('Only the endpoints below are automatically contacted. Country portal bookmarks are not automated integrations.')
    for s in SOURCES:
        h=health.get(s['id'],{})
        with st.expander(f"{s['country']} — {s['name']} · {'Fetch OK' if h.get('ok') else 'Not validated'}"):
            st.write('**Declared scope:** '+s['scope'])
            st.write('**Endpoint:** '+s['url'])
            st.write('**Items observed:** '+str(h.get('raw_items','Not scanned')))
            if h.get('error'):st.error(h['error'])
            st.link_button('Open official source',s['url'])

else:
    st.subheader('Evidence and legal review protocol')
    st.markdown('''**1. Authenticity:** Establish exact issuing authority, act identifier, original and amendment URLs.\n\n**2. Change detection:** Compare the newly published amendment with the version it changes; record affected article numbers and exact evidence passages.\n\n**3. Applicability:** Identify relevant jurisdictions, product types, economic operator roles, exemptions and transition provisions.\n\n**4. Review:** Require a named qualified reviewer before marking a legal assessment as approved.\n\n**5. Coverage audit:** Reconcile publication counts with government gazette indexes, test historical known changes, and track late/failed pages.\n\n**6. Escalation:** For possible market blocking, labeling changes or product testing, escalate to legal/compliance experts.''')
    st.warning('The app intentionally has no “AI legally verified” button. Automated legal analysis must remain pending until substantiated against primary source text and expert-reviewed.')
