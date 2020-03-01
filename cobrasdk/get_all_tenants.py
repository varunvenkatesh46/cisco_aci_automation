#!/usr/bin/python
import requests
requests.packages.urllib3.disable_warnings()
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
session = LoginSession('https://198.18.133.200', 'admin', 'C1sco12345')
moDir = MoDirectory(session)
moDir.login()


# set query to tenant class
from cobra.mit.request import ClassQuery
cq = ClassQuery('fvTenant')

# submit query
tenants = moDir.query(cq)

# print all tenants by name
for tenant in tenants:
    print(tenant.name)
