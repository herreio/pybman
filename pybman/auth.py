import json
import atexit
import requests

from pybman.rest import api_login
from pybman.rest import api_logout

from pybman import utils


class Auth:

    def __init__(self):

        # user data
        self.token = None
        self.grants = None
        self.roles = None

        # user credentials
        self.secret = None

        # read user credentials
        with open('conf/secret.json', 'r') as f:
            self.secret = json.load(f)

        # login via REST
        self.login()

        # get permission info
        self.permissions()

        # ensure logout at end of session
        atexit.register(self.logout)

    # func to login via REST
    def login(self):
        data = self.secret['user-pass']
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'}
        # response = utils.post_request(api_login, headers, data)
        response = requests.post(api_login, headers=headers, data=data)
        self.token = response.headers['Token']

    # func to request permission info
    def permissions(self):
        headers = {
            'accept': 'application/json',
            'Authorization': self.token}
        response = requests.get(api_login+'/who', headers=headers)
        grantlist = response.json()['grantList']
        grants = {}
        for grant in grantlist:
            if grant['role'] in grants:
                grants[grant['role']].append(grant['objectRef'])
            else:
                grants[grant['role']] = [grant['objectRef']]
        self.grants = grants
        self.roles = list(self.grants.keys())
        self.roles.sort()

    # func to logout via REST
    def logout(self):
        headers = {
            'accept': 'application/json',
            'Authorization': self.token}
        response = requests.get(api_logout, headers=headers)
        print(response.text)
