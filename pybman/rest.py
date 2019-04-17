import atexit

from pybman import utils
from copy import deepcopy


class BaseController:

    def __init__(self, url='https://pure.mpg.de/'):
        self.records = []

        # base url
        self.url = url
        self.format = {'format': 'json'}
        self.content = {"Content-Type": "application/json"}

        # self.format_query = {'format':'json', 'q':''}
        # self.scroll_query = {"scroll":"true"}


class RestController(BaseController):

    def __init__(self):

        super().__init__()

        # rest interface
        self.rest = self.url + 'rest/'


class LoginRestController(RestController):

    def __init__(self, auth=True, cred='conf/secret.json'):

        super().__init__()

        self.auth = auth

        # endpoints
        self.rest_login = self.rest + 'login'
        self.rest_login_who = self.rest_login + '/who'
        self.rest_logout = self.rest + 'logout'

        # user credentials
        self.secret = None

        # user data
        self.token = None
        self.grants = None
        self.roles = None

        # user status
        self.online = False

        self.accept = {'accept': 'application/json'}
        self.header = {'accept': 'application/json', 'Content-Type': 'application/json'}
        self.auth_header = deepcopy(self.accept)

        if auth:
            # read user credentials
            self.secret = utils.read_json(cred)
            # login via REST
            self.login()
            # get permission info
            self.get_user()
            # ensure logout at end of session
            atexit.register(self.logout)

    def login(self):
        if self.secret:
            data = self.secret['user-pass']
            response = utils.post_request(self.rest_login, headers=self.header, data=data, json_res=False)
            self.token = response.headers['Token']
            self.auth_header['Authorization'] = self.token
            self.online = True
        else:
            print("login failed! please provide credentials!")

    def get_user(self):
        if self.online:
            response = utils.get_request(self.rest_login_who, headers=self.auth_header)
            grantlist = response['grantList']
            grants = {}
            for grant in grantlist:
                if grant['role'] in grants:
                    grants[grant['role']].append(grant['objectRef'])
                else:
                    grants[grant['role']] = [grant['objectRef']]
            self.grants = grants
            self.roles = list(self.grants.keys())
            self.roles.sort()
        else:
            print("you need to be logged in to get user info!")

    # func to logout via REST
    def logout(self):
        if self.online:
            response = utils.get_request(self.rest_logout, headers=self.auth_header, json_response=False)
            print(response.text)
            self.online = False
        else:
            print("you need to be logged in to log out!")


class ItemRestController(LoginRestController):

    def __init__(self, secret):

        if secret:
            super().__init__(cred=secret)
        else:
            super().__init__(auth=False)

        # items endpoint
        self.rest_items = self.rest + 'items/'
        self.rest_items_release = self.rest_items + '$/release'
        self.rest_items_search = self.rest_items + 'search?'
        self.rest_items_search_scroll = self.rest_items + 'search/scroll?'

        self.params = {'format': 'json', 'scroll': 'true'}
        self.header = {"accept": "application/json", "Content-Type": "application/json"}
        self.query = {"query": {"term": {"context.objectId": {"value": "ctx_924547", "boost": 1.0}}},
                      "size": "50", "from": "0"}

    def search_items(self, query=None):
        self.records = []
        url = self.rest_items_search  # + params
        params = self.params
        headers = self.header
        if query:
            data = query
        else:
            data = self.query
        response = utils.post_request(url, params, headers, data)
        if 'scrollId' in response:
            scroll_id = response['scrollId']
            if 'records' in response:
                self.records += response['records']
                self.scroll_items(scroll_id, 1)
            else:
                return response
        else:
            return response

    # func to repeatedly request items
    def scroll_items(self, scroll_id, counter):
        print("scrolling for the "+str(counter)+". time...")
        headers = self.header
        params = self.format
        params['scrollId'] = scroll_id
        url = self.rest_items_search_scroll
        response = utils.get_request(url, params, headers)
        if 'records' in response:
            self.records += response['records']
            self.scroll_items(response['scrollId'], counter+1)

    def update_item(self, item_id, data):
        if self.auth:
            headers = self.content
            headers['Authorization'] = self.token
            url = self.rest_items + item_id
            return utils.put_request(url, headers, data)
        else:
            print("you need to be authorized to update items!")
            return None

    def release_item(self, item_id, data, comment):
        if self.auth:
            headers = self.content
            headers['Authorization'] = self.token
            url = self.rest_items_release.replace('$', item_id)
            params = {'comment': comment, 'lastModificationDate': data['lastModificationDate']}
            passphrase = self.secret['user-pass'].split(":")[1]
            params['password'] = passphrase
            return utils.put_request(url, headers, params)
        else:
            print("you need to be authorized to release items!")
            return None

    def revise_item(self):
        pass

    def submit_item(self):
        pass

    def withdraw_item(self):
        pass


class OrgUnitRestController(RestController):

    def __init__(self):

        super().__init__()

        # organisational units endpoint
        self.rest_org_units = self.rest + 'ous/'
        self.rest_org_units_search = self.rest_org_units + 'search/'
        self.rest_org_units_children = self.rest_org_units + '$/children'
        self.rest_org_units_toplevel = self.rest_org_units + 'toplevel'

    def get_all(self):
        res = utils.get_request(self.rest_org_units)
        size = {"size": res['numberOfRecords']}
        return utils.get_request(self.rest_org_units + "?", size)

    def get(self, ou_id='ou_907574'):
        url = self.rest_org_units + ou_id
        return utils.get_request(url)

    def top_level(self):
        return utils.get_request(self.rest_org_units_toplevel)

    def child_organizations(self, ou_id='ou_907574'):
        url = self.rest_org_units_children.replace('$', ou_id)
        return utils.get_request(url)


class ContextRestController(RestController):

    def __init__(self):

        super().__init__()

        # context endpoint
        self.rest_contexts = self.rest + 'contexts/'

    def get(self, ctx_id='ctx_924547'):
        url = self.rest_contexts + ctx_id
        return utils.get_request(url)

    def get_all(self):
        res = utils.get_request(self.rest_contexts)
        size = {"size": res['numberOfRecords']}
        return utils.get_request(self.rest_contexts + "?", size)


class FeedRestController(RestController):

    def __init__(self):

        super().__init__()

        self.rest_feed = self.rest + 'feed/'
        self.rest_feed_oa = self.rest_feed + 'oa'
        self.rest_feed_organization = self.rest_feed + 'organization/$'
        self.rest_feed_recent = self.rest_feed + 'recent'
        self.rest_feed_search = self.rest_feed + 'search'

    def get_recent_oa(self):
        pass

    def get_recent_releases_for_ou(self):
        pass

    def get_recent_releases(self):
        pass

    def get_search_as_feed(self):
        pass


class ConeController(BaseController):

    def __init__(self):

        super().__init__()

        # cone interface
        self.cone = self.url + 'cone/'


class PersonConeController(ConeController):

    def __init__(self):

        super().__init__()

        # persons endpoint
        self.cone_persons = self.cone + 'persons/'
        self.cone_persons_all = self.cone_persons + 'all?'
        self.cone_persons_query = self.cone_persons + 'query?'
        self.cone_persons_resource = self.cone_persons + 'resource/'

    def get_entities(self):
        return utils.get_request(self.cone_persons_all, self.format)

    def get_entity(self, person_id='persons32341'):
        url = self.cone_persons_resource + person_id + '?'
        return utils.get_request(url, self.format)

    def search_entity(self, cone_id):
        pass


class JournalConeController(ConeController):

    def __init__(self):

        super().__init__()

        # journals endpoint
        self.cone_journals = self.cone + 'journals/'
        self.cone_journals_all = self.cone_journals + 'all?'
        self.cone_journals_query = self.cone_journals + 'query?'
        self.cone_journals_resource = self.cone_journals + 'resource/'

    def get_entities(self):
        return utils.get_request(self.cone_journals_all, self.format)

    def get_entity(self, journal_id='954928372938'):
        url = self.cone_journals_resource + journal_id + '?'
        return utils.get_request(url, self.format)

    def search_entity(self, cone_id):
        pass
