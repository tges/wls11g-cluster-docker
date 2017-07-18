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

print "==> ADMINSERVER_URL = " + adminURL
print "==> WLS_ADMIN = " + adminUsername
print "==> WLS_PASSWD = " + adminPassword

# Connect to AdminServer.
connect(adminUsername, adminPassword, adminURL)


## DataSource Deploy
# Load the properties from the properties file.
datasourcePropPath = '/home/weblogic/datasources'



if os.path.isdir(datasourcePropPath):
  edit()
  startEdit()
  
  propfiles = [f for f in os.listdir(datasourcePropPath) if os.path.isfile(os.path.join(datasourcePropPath, f))]
  for i in range(0, len(propfiles)):
    print 'datasource properties = ' + propfiles[i]
    
  for properties in propfiles:
  
    # Load the properties from the properties file.
    from java.io import FileInputStream
  
    propInputStream = FileInputStream('/home/weblogic/datasources/' + properties)
    configProps = Properties()
    configProps.load(propInputStream)

    # Set all variables from values in properties file.
    dsName=configProps.get("ds.name")
    dsJNDIName=configProps.get("ds.jndi.name")
    dsURL=configProps.get("ds.url")
    dsDriver=configProps.get("ds.driver")
    dsUsername=configProps.get("ds.username")
    dsPassword=configProps.get("ds.password")
    
    dsMinimumCapacity=configProps.get("ds.minimum_capacity")
    dsMaximumCapacity=configProps.get("ds.maximum_capacity")
    dsInitialCapacity=configProps.get("ds.initial_capacity")
    
    dsTestConnectionsOnReserve=configProps.get("ds.test_connections_on_reserve")
    dsTestFrequency=configProps.get("ds.test_frequency")
    dsTestTableName=configProps.get("ds.test_table_name")
    dsSecondsToTrustAnIdlePoolConnection=configProps.get("ds.seconds_to_trust_an_idle_pool_connection")
    dsShrinkFrequency=configProps.get("ds.shrink_frequency")
    dsConnectionCreationRetryFrequency=configProps.get("ds.connection_creation_retry_frequency")
    dsInactiveConnectionTimeout=configProps.get("ds.inactive_connection_timeout")
    dsConnectionReserveTimeout=configProps.get("ds.connection_reserve_timeout")
    dsProfileConnectionLeak=configProps.get("ds.profile_connection_leak")
    
    
    dsTargetType='Cluster'
    dsTargetName='base_cluster'

    # Display the variable values.
    print '==================================='
    print 'adminUsername=', adminUsername
    print 'adminPassword=', adminPassword
    print 'adminURL=', adminURL
    print 'dsName=', dsName
    print 'dsJNDIName=', dsJNDIName
    print 'dsURL=', dsURL
    print 'dsDriver=', dsDriver
    print 'dsUsername=', dsUsername
    print 'dsPassword=', dsPassword
    print 'dsTargetType=', dsTargetType
    print 'dsTargetName=', dsTargetName
    print '==================================='
    
    # Create data source.
    cd('/')
    cmo.createJDBCSystemResource(dsName)

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
    cmo.setName(dsName)

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    set('JNDINames',jarray.array([String(dsJNDIName)], String))

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
    cmo.setUrl(dsURL)
    cmo.setDriverName(dsDriver)
    set('Password', dsPassword)
     
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
    cmo.setMinCapacity(int(dsMinimumCapacity))
    cmo.setMaxCapacity(int(dsMaximumCapacity))
    cmo.setInitialCapacity(int(dsInitialCapacity))
    cmo.setTestConnectionsOnReserve(bool(dsTestConnectionsOnReserve))
    cmo.setTestFrequencySeconds(int(dsTestFrequency))
    cmo.setTestTableName('SQL ' + dsTestTableName + '\r\n\r\n')
    cmo.setSecondsToTrustAnIdlePoolConnection(int(dsSecondsToTrustAnIdlePoolConnection))
    cmo.setShrinkFrequencySeconds(int(dsShrinkFrequency))
    cmo.setConnectionCreationRetryFrequencySeconds(int(dsConnectionCreationRetryFrequency))
    cmo.setInactiveConnectionTimeoutSeconds(int(dsInactiveConnectionTimeout))
    cmo.setConnectionReserveTimeoutSeconds(int(dsConnectionReserveTimeout))
    
    if bool(dsProfileConnectionLeak) == true:
      cmo.setProfileType(0x000004)
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
    cmo.createProperty('user')

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
    cmo.setValue(dsUsername)

    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')

    cd('/SystemResources/' + dsName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + dsTargetName + ',Type=' + dsTargetType)], ObjectName))

  save()
  activate()

## Application Deploy
deploymentPath = '/home/weblogic/deployments'

if os.path.isdir(deploymentPath):

  edit()
  startEdit()
  
  deployments = os.listdir(deploymentPath)
  for i in range(0, len(deployments)):
    print 'deployment ======> ' + deployments[i]

    appName = deployments[i]
    warPath = deploymentPath + '/' + deployments[i]

    deploy(appName, path = warPath, targets='base_cluster')

  save()
  activate()

disconnect()
exit()
