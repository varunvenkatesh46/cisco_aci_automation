from acilib import *
import yaml
import json

if __name__ == "__main__":
    data = yaml.safe_load(open('../data/DEMO_tenant.yaml'))

    token = get_cookies()

    create_tenant(data['Tenant'],token)

    create_vrf(data['VRF'],token)

    create_bd(data['BD'],token)

    for subnet in data['Subnets']:
        create_bd_subnet(subnet,token)

    create_anp(data['ANP'],token)

    for epg in data['EPGs']:
        create_epg(epg,token)

    for filter in data['Filters']:
        create_filter(filter,token)

    for filterentry in data['FilterEntries']:
        create_filterentry(filterentry,token)

    for contract in data['Contracts']:
        create_contract(contract,token)

    for subject in data['Subjects']:
        create_contract_subject(subject,token)

    for subjectentry in data['SubjectEntries']:
        create_contract_subject_entry(subjectentry,token)

    for bindcontract in data['BindContracts']:
        create_bindcontract(bindcontract,token)

    #delete_tenant(data['Tenant'],token)
