import requests
from ACI.native.codes.acilib import *
import json
import yaml
from jinja2 import Environment, FileSystemLoader
from ACI.native.codes.aciconnection import apic

cookies = get_cookies()

uri = '/api/node/mo/uni/infra.json'
url = apic + uri

env = Environment(loader=FileSystemLoader('../templates'), trim_blocks=True, lstrip_blocks=True)
config_data = yaml.safe_load(open('discovery2.yaml'))

policies = ['intlinkpolicy.json',
            'cdppolicy.json',
            'lldppolicy.json',
            'portchannel.json',
            'vpc_pol_grp.json',
            'int_profile.json',
            'int_selector.json',
            'switch_profile.json',
            'vpc_default.json']

for policy in policies:
    template = env.get_template(policy)
    payload = json.loads(template.render(config_data))

    print('EXECUTING POST ', url)
    #print('PAYLOAD:\n', json.dumps(payload, indent=2))
    req = requests.post(url, cookies=cookies, data=json.dumps(payload), verify=False)

    if req.status_code == 200:
        print(policy.split('.')[0].upper(), ' applied sucessfuly\n\n')
        print('-------------------------------------------------------')
    else:
        print(policy.split('.')[0].upper(), ' not applied', ' Status Code: ', req.status_code, req.raise_for_status())
        print('-------------------------------------------------------')
    #input('Press Any Key to Continue:')
