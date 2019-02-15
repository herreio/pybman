from pybman.utils import read_json
from pybman.local import resolve_path

# search query templates
ou_query = resolve_path('static/elastic/ou.json')
ctx_query = resolve_path('static/elastic/ctx.json')
pers_query = resolve_path('static/elastic/pers.json')

# get organisation query with given id
def get_ou_query(ou_id):
    data = read_json(ou_query)
    term = data['query']['bool']['must'][2]['bool']['should'][0]['term']
    term['metadata.creators.person.organizations.identifierPath']['value'] = ou_id
    term = data['query']['bool']['must'][2]['bool']['should'][1]['term']
    term['metadata.creators.organization.identifierPath']['value'] = ou_id
    return data

# get context query with given id
def get_ctx_query(ctx_id):
    data = read_json(ctx_query)
    data['query']['bool']['must'][2]['term']['context.objectId']['value'] = ctx_id
    return data

def get_pers_query(pers_id):
    data = read_json(pers_query)
    data['query']['bool']['must'][2]['term']['metadata.creators.person.identifier.id']['value'] = pers_id
    return data
