from pybman import utils
from pybman.auth import Auth

from urllib.parse import urlencode
# from pybman.utils import get_request, post_request

class Controller:

    def __init__(self, auth=False):

        self.auth = None
        self.records = []

        if auth:
            self.auth = Auth()

        # base url
        self.url = 'https://pure.mpg.de/'

        # rest interface
        self.rest = self.url + 'rest/'

        # login endpoint
        self.rest_login = self.rest + 'login'

        # logout endpoint
        self.rest_logout = self.rest + 'logout'

        # items endpoint
        self.rest_items = self.rest + 'items/'
        self.rest_items_search = self.rest_items + 'search?'
        self.rest_items_search_scroll = self.rest_items + 'search/scroll?'

        # context endpoint
        self.rest_contexts = self.rest + 'contexts/'

        # organisational units endpoint
        self.rest_org_units = self.rest + 'ous/'
        self.rest_org_units_search = self.rest_org_units + 'search/'
        self.rest_org_units_chlildren = self.rest_org_units + '$/children'
        self.rest_org_units_toplevel = self.rest_org_units + 'toplevel'

        # cone interface
        self.cone = self.url + 'cone/'

        # persons endpoint
        self.cone_persons = self.cone + 'persons/'
        self.cone_persons_all = self.cone_persons + 'all?'
        self.cone_persons_query = self.cone_persons + 'query?'
        self.cone_persons_resource = self.cone_persons + 'resource/'

        # journals endpoint
        self.cone_journals = self.cone + 'journals/'
        self.cone_journals_all = self.cone_journals + 'all?'
        self.cone_journals_query = self.cone_journals + 'query?'
        self.cone_journals_resource = self.cone_journals + 'resource/'

        self.format = {'format':'json'}
        self.params = {'format':'json', 'scroll':'true'}
        self.query = {"query": {"term":{"context.objectId":{"value":"ctx_924547","boost":1.0}}},
                    "sort": [{"metadata.genre":{"order":"ASC"},"sort-metadata-dates-by-category":{
                    "order":"ASC"},"sort-metadata-creators-compound":{"order":"ASC"}}],"size":"50","from":"0"}
        self.header = {"accept": "application/json","Content-Type":"application/json"}
        # self.format_query = {'format':'json', 'q':''}
        #  self.scroll_query = {"scroll":"true"}

    def search_items(self, query):
        self.records = []
        url = self.rest_items_search # + params
        params = self.params
        headers = self.header
        data = self.query
        response = utils.post_request(url, params, headers, data)
        scrollId = response['scrollId']
        self.records += response['records']
        self.scroll_items(scrollId, 1)

    # func to repeatedly request items
    def scroll_items(self, scrollId, counter):
        print("scrolling for the "+str(counter)+". time...")
        headers = self.header
        params = self.format
        params['scrollId'] = scrollId
        url = self.rest_items_search_scroll
        response = utils.get_request(url,params,headers)
        if 'records' in response:
            self.records += response['records']
            self.scroll_items(response['scrollId'], counter+1)

    def get_ctxs(self):
        return utils.get_request(self.rest_contexts)

    def get_ous():
        return utils.get_request(self.rest_org_units)

    def get_ous_toplevel():
        return utils.get_request(self.rest_org_units_toplevel)

    def get_ou_info(ou_id='ou_907574'):
        url = self.rest_org_units + ou_id
        return utils.get_request(url)

    def get_ou_children(ou_id='ou_907574'):
        url = self.rest_org_units_children.replace('$',ou_id)
        return utils.get_request(url)

    def get_ctx_info(ctx_id='ctx_924547'):
        url = self.rest_contexts + ctx_id
        return utils.get_request(url)

    def get_cone_journals(self):
        return utils.get_request(self.cone_journals_all, self.format)

    def get_cone_persons(self):
        return utils.get_request(self.cone_persons_all, self.format)

    def get_cone_journal_info(self, journal_id='954928372938'):
        url = self.cone_journals_resource + journal_id + '?'
        return utils.get_data(url, rest.format)

    def get_cone_person_info(self, person_id='persons32341'):
        url = self.cone_persons_resource + person_id + '?'
        return utils.get_data(url, rest.format)

    def search_person(self, cone_id):
        pass

    def search_journal(self, cone_id):
        pass
