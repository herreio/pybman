from pybman import rest
from pybman import search

# get remote data: context by id
def get_ctx(ctx_id):
    header = rest.post_header()
    data = search.get_ctx_query(ctx_id)
    print("request context data:")
    result = rest.post_data(rest.items_search,header,data)
    return result

# get remote data: organisation by id
def get_ou(ou_id):
    header = rest.post_header()
    data = search.get_ou_query(ou_id)
    print("request organisation data:")
    result = rest.post_data(rest.items_search,header,data)
    return result

def get_pers(pers_id):
    header = rest.post_header()
    data = search.get_pers_query(pers_id)
    print("request person data:")
    result = rest.post_data(rest.items_search,header,data)
    return result

def get_ctxs():
    return rest.get_data(rest.contexts)

def get_ous():
    return rest.get_data(rest.org_units)

def get_ous_toplevel():
    return rest.get_data(rest.org_units_toplevel)

def get_ou_info(ou_id='ou_907574'):
    url = rest.org_units + ou_id
    return rest.get_data(url)

def get_ou_children(ou_id='ou_907574'):
    url = rest.org_units_chldrn.replace('$',ou_id)
    return rest.get_data(url)

def get_ctx_info(ctx_id='ctx_924547'):
    url = rest.contexts + ctx_id
    return rest.get_data(url)

def get_journals():
    return rest.get_data_with_params(rest.cone_journals_all, rest.format)

def get_persons():
    return rest.get_data_with_params(rest.cone_persons_all, rest.format)

def get_journal_info(journal_id='954928372938'):
    url = rest.cone_journals_resource + journal_id + '?'
    return rest.get_data_with_params(url,rest.format)

def get_person_info(person_id='persons32341'):
    url = rest.cone_persons_resource + person_id + '?'
    return rest.get_data_with_params(url,rest.format)

def search_person(cone_id):
    pass

def search_journal(cone_id):
    pass
