#!/usr/bin/python3
import requests
requests.packages.urllib3.disable_warnings()

from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession


session = LoginSession('https://192.168.10.1', 'admin', 'C1sco12345')
moDir = MoDirectory(session)
moDir.login()


from cobra.mit.request import ConfigRequest
configReq = ConfigRequest()


from cobra.model.fv import Tenant


uniMo = moDir.lookupByDn('uni')

fvTenantMo = Tenant(uniMo, 'DEMO-COBRA')
fvTenantMo.delete()
configReq.addMo(fvTenantMo)
moDir.commit(configReq)


