import json
import requests

from urllib.parse import urlencode

base = 'https://pure.mpg.de/'

# rest interface
api = base + 'rest/'

items = api + 'items/'
items_search = items + 'search?'

contexts = api + 'contexts/'

org_units = api + 'ous/'
org_units_search = org_units + 'search/'
org_units_chldrn = org_units + '$/children'
org_units_toplevel = org_units + 'toplevel'

# cone interface
cone = base + 'cone/'

cone_persons = cone + 'persons/'
cone_persons_all = cone_persons + 'all?'
cone_persons_query = cone_persons + 'query?'
cone_persons_resource = cone_persons + 'resource/'

cone_journals = cone + 'journals/'
cone_journals_all = cone_journals + 'all?'
cone_journals_query = cone_journals + 'query?'
cone_journals_resource = cone_journals + 'resource/'

format = {'format':'json'}
format_query = {'format':'json', 'q':''}
scroll_query = {"scroll":"true"}


# send get request to fetch data
def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("something went wrong while requesting data!")
        return {}

# send get request with parameters
def get_data_with_params(url,params):
    params = urlencode(params)
    url = url + params
    return get_data(url)

# send a post request to fetch data
def post_data(url,header,data):
    payload = json.dumps(data)
    print("request with offset: 0")
    response = requests.post(url,headers=header,data=payload)
    result = response.json()
    total = result['numberOfRecords']
    # print("total:",total)
    if total > 0:
        offset = len(result['records'])
        while offset < total:
            print("request with offset:",offset)
            data['from'] = str(offset)
            records = get_records(url, header, data)
            result['records'] += records
            offset = len(result['records'])
        print("found",offset, "items!")
    else:
        result = {'numberOfRecords':0,'records':[]}
    return result


# get post request header
def post_header():
    return {'Cache-Control': 'no-cache',
            'accept': 'application/json',
            'Content-Type': 'application/json'}

# request records with given offset
def get_records(url,header,data):
    payload = json.dumps(data)
    response = requests.post(url,headers=header,data=payload)
    if response.status_code == 200:
        result = response.json()
        if 'records' in result:
            return result['records']
        else:
            print("no records in response!")
            return []
    else:
        print("something went wrong while fetching data!")
        return []
