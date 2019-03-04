from pybman import utils
from copy import deepcopy

# class Query:
#
#    def __init__(self):
#        pass
#
#    def read_query(self, file_path):
#        return utils.read_json(file_path)

class ContextQuery:

    def __init__(self):

        self.item_query_fp = utils.resolve_path('static/elastic/item-ctx.json')
        self.item_released_query_fp = utils.resolve_path('static/elastic/item-ctx-released.json')

        self.item_query = utils.read_json(self.item_query_fp)
        self.item_released_query = utils.read_json(self.item_released_query_fp)

    def get_item_query(self, ctx_id):
        data = deepcopy(self.item_query)
        data['query']['term']['context.objectId']['value'] = ctx_id
        return data

    def get_released_item_query(self, ctx_id):
        data = deepcopy(self.item_released_query)
        data['query']['bool']['must'][2]['term']['context.objectId']['value'] = ctx_id
        return data


class OrgUnitQuery:

    def __init__(self):

        self.item_query_fp = utils.resolve_path('static/elastic/item-ou.json')
        self.item_released_query_fp = utils.resolve_path('static/elastic/item-ou-released.json')

        self.item_query = utils.read_json(self.item_query_fp)
        self.item_released_query = utils.read_json(self.item_released_query_fp)

    def get_item_query(self, ou_id):
        """
        ! to do !
        """
        data = deepcopy(self.item_query)
        # ... fill in ou_id ...
        return data

    def get_item_released_query(self, ou_id):
        data = deepcopy(self.item_released_query)
        term = data['query']['bool']['must'][2]['bool']['should'][0]['term']
        term['metadata.creators.person.organizations.identifierPath']['value'] = ou_id
        term = data['query']['bool']['must'][2]['bool']['should'][1]['term']
        term['metadata.creators.organization.identifierPath']['value'] = ou_id
        return data

class PersQuery:

    def __init__(self):
        pass