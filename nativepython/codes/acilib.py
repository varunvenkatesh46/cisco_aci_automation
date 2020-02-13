import requests
import json
from aciconnection import apic, uri, username, password, url
from acicrud import acipost, acidelete, aciget

requests.packages.urllib3.disable_warnings()  # Suppress SSL Warning


def get_cookies():
    url2 = apic + '/api/aaaLogin.json'
    payload = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))
    print('\nPOST Login: ', url2)
    req = requests.post(url2, data=json.dumps(payload), verify=False)
    if req.cookies:
        print('Login Successful.')
    return req.cookies


def get_tenants(cookies):
    print('\nExecuting GET ', url)
    req = requests.get(url, cookies=cookies, verify=False)
    return req


def get_tenant(payload, cookies):
    req = aciget(payload, cookies)
    return req


def create_tenant(payload, cookies):
    print('\nCreating Tenant: ', payload['fvTenant']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def delete_tenant(payload, cookies):
    req = acidelete(payload, cookies)
    return req


def create_vrf(payload, cookies):
    print('\nCreating VRF: ', payload['fvCtx']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def create_bd(payload, cookies):
    print('\nCreating Bridge Domain: ', payload['fvBD']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def create_bd_subnet(payload, cookies):
    print('\nCreating Subnet:', payload['fvSubnet']['attributes']['ip'])
    req = acipost(url, payload, cookies)
    return req


def create_anp(payload, cookies):
    url = apic + uri
    print('\nCreating Application Profile:', payload['fvAp']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def create_epg(payload, cookies):
    url = apic + uri
    print('\nCreating End Point Group: ', payload['fvAEPg']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req

def create_filter(payload, cookies):
    print('\nCreating Filter:', payload['vzFilter']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def create_filterentry(payload, cookies):
    print('\nAdding Filter Entry: ', payload['vzEntry']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req

def create_contract(payload, cookies):
    print('\nCreating Contract:', payload['vzBrCP']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def create_contract_subject(payload, cookies):
    url = apic + uri
    print('\nAdding Subject: ', payload['vzSubj']['attributes']['name'])
    req = acipost(url, payload, cookies)
    return req


def create_contract_subject_entry(payload, cookies):
    url = apic + uri
    print('\nAdding Subject Entry: ', payload['vzRsSubjFiltAtt']['attributes']['tnVzFilterName'])
    req = acipost(url, payload, cookies)
    return req


def create_bindcontract(payload, cookies):
    url = apic + uri
    if 'fvRsCons' in payload.keys():
        conkey = 'fvRsCons'
        print('\nApplying Consumer Contract: ', payload[conkey]['attributes']['tnVzBrCPName'])
    else:
        conkey = 'fvRsProv'
        print('\nApplying Provider Contract: ', payload[conkey]['attributes']['tnVzBrCPName'])
    req = acipost(url, payload, cookies)
    return req


