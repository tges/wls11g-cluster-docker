#!/usr/bin/python
import re
import os
import time
import getopt
import sys
import datetime

## Global Properties
adminUsername = os.environ['WLS_ADMIN']
adminPassword = os.environ['WLS_PASSWD']

# Connect to AdminServer.
connect(adminUsername, adminPassword)

## Check Managed Server Status
serverNames = cmo.getServers()
domainRuntime()

s = datetime.datetime.now()
print '[' + str(s) + '][PURGE] Fetching state of every WebLogic instance which is UNKNOWN state'

unknowns = []

for name in serverNames:
  cd("/ServerLifeCycleRuntimes/" + name.getName())
  serverState = cmo.getState()
  if serverState == "UNKNOWN":
    s = datetime.datetime.now()
    print "[" + str(s) + "][PURGE] Server " + name.getName() + " is [" + serverState + "], will be deleted.."
    unknowns.append(name)

serverConfig()

edit()
startEdit()

## Destroy Server
for unknownServer in unknowns:
  cd('/Servers/' + unknownServer.getName())
  cmo.setCluster(None)
  cmo.setMachine(None)
  editService.getConfigurationManager().removeReferencesToBean(getMBean('/Servers/' + unknownServer.getName()))
  
  cd('/')
  cmo.destroyServer(unknownServer)

save()
activate()



disconnect()
exit()
