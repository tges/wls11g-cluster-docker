#!/bin/bash

## check weblogic server is running
sleep 120

while :
do
    state=`java -classpath ${ORACLE_HOME}/wlserver_10.3/server/lib/weblogic.jar weblogic.Admin -url t3://${ADMINSERVER_URL} -username ${WLS_ADMIN} -password ${WLS_PASSWD} GETSTATE| cut -d\: -f2`
    if [[ "$state" == *RUNNING* ]];
    then
        ${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh ${DOMAIN_HOME}/scripts/purge_managed_server.py
    fi
    sleep 60
done



