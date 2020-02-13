import requests
import json
from ACI.native.codes.aciconnection import apic, uri, username, password, url
from ACI.native.codes.acicrud import acipost

requests.packages.urllib3.disable_warnings()  # Suppress SSL Warning


# def get_cookies():
#     url2 = apic + '/api/aaaLogin.json'
#     payload = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))
#     req = requests.post(url2, data=json.dumps(payload), verify=False)
#     #print(json.dumps(req.json(),indent=4))
#     cookies = req.json()['imdata'][0]['aaaLogin']['attributes']['token']
#     #print(cookies)
#     return cookies

def get_cookies():
    url2 = apic + '/api/aaaLogin.json'
    payload = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))
    req = acipost(url2, payload)
    #print(json.dumps(req.json(),indent=4))
    cookies = req.json()['imdata'][0]['aaaLogin']['attributes']['token']
    return cookies


def create_tenant(payload, cookies):
    print('\nCreating Object ', payload['fvTenant']['attributes']['name'])
    req = acipost(url, payload, cookies)


print(get_cookies())