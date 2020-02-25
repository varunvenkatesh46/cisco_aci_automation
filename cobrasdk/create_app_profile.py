#!/usr/bin/python3
import requests
import yaml
requests.packages.urllib3.disable_warnings()

# Import access classes
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest

# Import model classes
from cobra.model.fvns import VlanInstP, EncapBlk
from cobra.model.infra import RsVlanNs
from cobra.model.fv import Tenant, Ctx, BD, RsCtx, Ap, AEPg, RsBd, RsDomAtt, RsCons, RsProv
from cobra.model.vmm import DomP, UsrAccP, CtrlrP, RsAcc
from cobra.model.vz import Filter, Entry, BrCP, Subj, RsSubjFiltAtt


data = yaml.safe_load(open('vars/demo.yml'))
tenant = data['tenant_info']

session = LoginSession('https://198.18.133.200', 'admin', 'C1sco12345')
moDir = MoDirectory(session)
moDir.login()


configReq = ConfigRequest()
uniMo = moDir.lookupByDn('uni')


fvTenantMo = Tenant(uniMo, tenant['name'])

# Import the Ap class from the model
for anp in tenant['anps']:
    print('Creating App Profile', anp['name'])
    fvApMo = Ap(fvTenantMo, anp['name'])
    for epg in anp['epgs']:
        # Import the AEPg class from the model
        print('Creating EPG', epg['name'])
        fvAEPgMo = AEPg(fvApMo, epg['name'])
        print('Associate EPG', epg['name'], 'To Bridge Domain', epg['bd'] )
        fvRsBdMo = RsBd(fvAEPgMo, tnFvBDName = epg['bd'])
        if epg.get('conscontracts'):
            for conscontract in epg['conscontracts']:
                print('Associating Consumer Contract', conscontract, 'To EPG',epg['name'])
                fvRsConsMo = RsCons(fvAEPgMo, tnVzBrCPName=conscontract )
        if epg.get('provcontracts'):
            for provcontract in epg['provcontracts']:
                print('Associating Provider Contract', provcontract, 'To EPG',epg['name'])
                fvRsPovsMo = RsProv(fvAEPgMo, tnVzBrCPName=provcontract )
    configReq.addMo(fvApMo)


for filter in tenant['filters']:
    # create filter
    vzFilterMo = Filter(fvTenantMo, filter['name'])
    for entry in filter['entries']:
        # create filter Entry
        vzEntryMo = Entry(vzFilterMo, entry['name'])
        vzEntryMo.dFromPort = entry.get('dFromPort')   # HTTP port
        vzEntryMo.dToPort = entry.get('dToPort')
        vzEntryMo.prot = entry.get('prot')         # TCP protocol number
        vzEntryMo.etherT = entry.get('etherT')     # EtherType
    configReq.addMo(vzFilterMo)

for contract in tenant['contracts']:
    # create a binary contract (vz.BrCP object) container within the tenant
    vzBrCPWeb = BrCP(fvTenantMo, contract['name'])
    for subject in contract['subjects']:
        # create a subject container for associating the filter with the contract
        vzSubjMo = Subj(vzBrCPWeb, subject['name'])
        for subj_filter in subject['filters']:
            RsSubjFiltAtt(vzSubjMo, tnVzFilterName=subj_filter)
    configReq.addMo(vzBrCPWeb)


moDir.commit(configReq)
