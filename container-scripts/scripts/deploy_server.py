#!/usr/bin/python
import re
import os
import time
import getopt
import sys

## Global Properties
adminURL = os.environ['ADMINSERVER_URL']
adminUsername = os.environ['WLS_ADMIN']
adminPassword = os.environ['WLS_PASSWD']
#serverName = os.environ['SERVER_NAME']
hostname = os.environ['HOSTNAME']
listenAddress = os.environ['POD_IP']
cluster = 'base_cluster'

# Connect to AdminServer.
connect(adminUsername, adminPassword, adminURL)

## Add Managed Server
# Display the variable values.
print 'adminUsername=', adminUsername
print 'adminPassword=', adminPassword
print 'adminURL=', adminURL
print 'hostname=', hostname
print 'listenAddress=', listenAddress


edit()
startEdit()

# Create the managed Server.
cd('/')
cmo.createServer(hostname)
cd('/Servers/' + hostname)
cmo.setListenAddress(listenAddress)
cmo.setListenPort(7001)
#cmo.getWebServer().setMaxRequestParamterCount(25000)

# Direct stdout and stderr.
cd('/Servers/' + hostname + '/Log/' + hostname)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')

# Associate with a cluster.
cd('/Servers/' + hostname)
cmo.setCluster(getMBean('/Clusters/base_cluster'))

# Manage logging.
cd('/Servers/' + hostname + '/Log/' + hostname)
cmo.setRotationType('byTime')
cmo.setFileCount(30)
cmo.setRedirectStderrToServerLogEnabled(true)
cmo.setRedirectStdoutToServerLogEnabled(true)
cmo.setMemoryBufferSeverity('Debug')
cmo.setLogFileSeverity('Notice')

save()
activate()



disconnect()
exit()
