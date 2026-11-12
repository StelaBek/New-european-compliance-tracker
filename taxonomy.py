"""European market registry and configurable e-commerce product taxonomy."""
EU = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czechia','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden']
OTHER_EEA = ['Iceland','Liechtenstein','Norway']
OTHER_EUROPE = ['Albania','Andorra','Armenia','Azerbaijan','Belarus','Bosnia and Herzegovina','Georgia','Kosovo','Moldova','Monaco','Montenegro','North Macedonia','San Marino','Serbia','Switzerland','Türkiye','Ukraine','United Kingdom','Vatican City']
COUNTRIES = ['European Union'] + sorted(set(EU+OTHER_EEA+OTHER_EUROPE))
# Taxonomy labels and bounded keywords are heuristic suggestions, never legal determinations.
CATEGORIES = {
 'Furniture & upholstery': ['furniture','upholster','sofa','seating','mattress','bedstead','flammability','ignition','furnishing','møbler','møbel','möbler','huonekalut','kaluste','paloturvallisuus'],
 'Toys & childcare': ['toy','childcare','nursery','playground','child safety','pram','stroller','leksaker','leketøy','lelut'],
 'Chemicals & materials': ['reach','chemical','substance','svhc','bisphenol','phthalate','pop regulation','persistent organic pollutant','clp regulation','hazardous substance'],
 'General product safety': ['general product safety','gpsr','product safety','market surveillance','product recall','product liability','consumer product','produktsäkerhet','produktsikkerhet','tuoteturvallisuus'],
 'Machinery & equipment': ['machinery','machine safety','powered tool','industrial equipment','machine regulation'],
 'Electrical & lighting': ['electrical','lighting','luminaire','low voltage','electromagnetic compatibility','electronic equipment','radio equipment','rohs','weee','elektrisk','elutrustning','sähkölaitteet'],
 'Packaging & EPR': ['packaging','packaged','extended producer responsibility','epr','producer responsibility','recycling fee','packaging waste','emballasje','förpackning','pakkaus','tuottajavastuu'],
 'Textiles & apparel': ['textile','clothing','garment','apparel','footwear','leather','fibre composition','fiber composition'],
 'Electronics & connected': ['wireless','connectivity','radio equipment','cyber resilience','smart device','digital product'],
 'Batteries & energy': ['battery','batteries','energy labelling','energy labeling','ecodesign'],
 'Food contact & kitchen': ['food contact','kitchenware','utensil','cookware','food-contact'],
 'Cosmetics & personal care': ['cosmetic','personal care','fragrance','beauty product'],
 'Sports, PPE & outdoor': ['protective equipment','ppe','bicycle','sports equipment','helmet','outdoor product'],
 'Medical & health products': ['medical device','in vitro diagnostic','health product'],
 'Construction & DIY': ['construction product','building product','paint','adhesive','do-it-yourself'],
 'Sustainability & digital passports': ['digital product passport','ecodesign','environmental claim','green claim','sustainability','deforestation'],
 'Other e-commerce products': []
}
TOPICS = {
 'Testing & standards':['standard','test method','conformity assessment','flammability','ignition','harmonised standard','harmonized standard'],
 'Chemical restrictions':['restriction','hazardous substance','svhc','reach','rohs','chemical'],
 'Labelling & information':['labelling','labeling','label','instruction','warning','traceability','declaration of conformity'],
 'Market access & recalls':['market surveillance','recall','prohibit','withdrawal','market access','product safety'],
 'EPR & waste':['extended producer responsibility','epr','waste','recycling','producer register'],
 'Digital passports':['digital product passport','product passport','digital traceability']
}
# Seed only feed endpoints confirmed from official documentation or official EUR-Lex feed.
STARTER_SOURCES = [
 dict(name='EUR-Lex — Official Journal L acts', country='European Union', kind='rss', url='https://eur-lex.europa.eu/EN/display-feed.rss?rssId=165', official_domain='eur-lex.europa.eu'),
 dict(name='UK legislation — New legislation', country='United Kingdom', kind='atom', url='https://www.legislation.gov.uk/new/data.feed', official_domain='legislation.gov.uk'),
 dict(name='Germany — Federal legislation updates', country='Germany', kind='rss', url='https://www.gesetze-im-internet.de/aktuDienst-rss-feed.xml', official_domain='gesetze-im-internet.de'),
 dict(name='Norway — Norsk Lovtidend new laws and regulations', country='Norway', kind='rss',url='https://lovdata.no/feed?data=LT&type=RSS',official_domain='lovdata.no'),
 dict(name='Sweden — Riksdag legislative documents API', country='Sweden', kind='riksdagen_api',url='https://data.riksdagen.se/dokumentlista/?utformat=json&sort=datum&sortorder=desc&sz=30',official_domain='data.riksdagen.se'),
 dict(name='Finland — Finlex new statute listing API', country='Finland', kind='finlex_api',url='https://opendata.finlex.fi/finlex/avoindata/v1/akn/fi/act/statute/list',official_domain='opendata.finlex.fi'),
]
