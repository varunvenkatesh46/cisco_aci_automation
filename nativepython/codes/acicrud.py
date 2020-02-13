import json
import requests
from aciconnection import apic

requests.packages.urllib3.disable_warnings()  # Suppress SSL Warning



def aciget(payload, cookies):
    k = list(payload.items())[0][0]
    uri = f"/api/mo/{payload[k]['attributes']['dn']}.json"
    url = apic + uri
    print('\nExecuting GET ', url)
    try:
        req = requests.get(url, cookies=cookies, verify=False)
        req.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return req

def acipost(url, payload, cookies):
    print('Executing POST ', url)
    try:
        req = requests.post(url, cookies=cookies, data=json.dumps(payload), verify=False)
        req.raise_for_status()
        if 'aaaLogin' not in url:
            check_objectcreation(req, payload)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return req


def acidelete(payload, cookies):
    k = list(payload.items())[0][0]
    uri = f"/api/mo/{payload[k]['attributes']['dn']}.json"
    url = apic + uri
    try:
        print('\nDeleting Object ', payload[k]['attributes']['dn'])
        print('Executing DELETE ', url)
        req = requests.delete(url, cookies=cookies, verify=False)
        check_objectdeletion(req, payload)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return req


def check_objectcreation(req, payload):
    k = list(payload.items())[0][0]
    if req.status_code == 200:
        print(f"Object {payload[k]['attributes']['dn']} created sucessfully.")
    else:
        print(f"Object {payload[k]['attributes']['dn']} creation unsucessfull. Response Code:", req.status_code)


def check_objectdeletion(req, payload):
    k = list(payload.items())[0][0]
    if req.status_code == 200:
        print(f"Object {payload[k]['attributes']['name']} deleted sucessfully.")
    else:
        print(f"Object {payload[k]['attributes']['name']} deleted unsucessfully.", req.status_code)
