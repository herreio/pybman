import json
import requests

from urllib.parse import urlencode

# write given list (results) to file at path
def write_list(path, results):
    print("write list to file", path)
    if type(results[0]) == str:
        with open(path, "w+", encoding="utf8") as f:
            f.write("\n".join(results))
    if type(results[0]) == list:
        with open(path, "w+", encoding="utf8") as f:
            for res in results:
                f.write('"' + '"\n"'.join(res) + '"\n')

# read plain text file
def read_plain_clean(path):
    print("read plain text file", path)
    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            lines.append(line.strip('\n'))
    return lines

# read json file at path
def read_json(path):
    print("read file", path)
    result = {}
    with open(path,'r',encoding='utf-8') as f:
        result = json.load(f)
    return result

# write given data to json file at path
def write_json(path, data):
    print("write to", path)
    with open(path, 'w', encoding="utf-8") as f:
        s = json.dumps(data, indent=2)
        f.write(s)
    return path

# send get request to fetch data
def get_request(url, params=None, headers=None, json_response=True):
    if params:
        params = urlencode(params)
        url = url + params
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        if json_response:
            return response.json()
        else:
            return response
    else:
        print("something went wrong while requesting data!")
        return {}

# send a post request with data
def post_request(url, params=None, headers=None, data=None, json_res=True):
    if params:
        params = urlencode(params)
        url = url + params
    if type(data) == dict:
        payload = json.dumps(data)
    else:
        payload = data
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        if json_res:
            return response.json()
        else:
            return response
    else:
        print("something went wrong while requesting data!")
        print("got status code", response.status_code,"!")
        return {}

def put_request(url, header, data):
    payload = json.dumps(data)
    response = requests.put(url,headers=header,data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("something went wrong while requesting data!")
