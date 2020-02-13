#!/usr/bin/python3
import requests
import yaml
requests.packages.urllib3.disable_warnings()

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession

data = yaml.safe_load(open('vars/demo.yml'))
tenant = data['tenant_info']

session = LoginSession('https://192.168.10.1', 'admin', 'C1sco12345')
moDir = MoDirectory(session)
moDir.login()


from cobra.mit.request import ConfigRequest
configReq = ConfigRequest()


from cobra.model.fv import Tenant
uniMo = moDir.lookupByDn('uni')
print('Creating Tenant', tenant['name'])
fvTenantMo = Tenant(uniMo, tenant['name'])

# Import the related classes from the model
from cobra.model.fv import RsBd, Ctx, BD, RsCtx, Subnet

# create a private network
for vrf in tenant['vrfs']:
    print('Creating VRF', vrf['name'])
    fvCtxMo = Ctx(fvTenantMo, vrf['name'])
    # create a bridge domain
    for bd in vrf['bds']:
        print('Creating BD', bd['name'])
        fvBDMo = BD(fvTenantMo, bd['name'])
        # create an association of the bridge domain to the private network
        fvRsCtx = RsCtx(fvBDMo, tnFvCtxName=fvCtxMo.name)

        # create subnet
        for subnet in bd['subnets']:
            print('Creating Subnet', subnet)
            fvSubnetMo = Subnet(fvBDMo, subnet)

configReq.addMo(fvTenantMo)
moDir.commit(configReq)


