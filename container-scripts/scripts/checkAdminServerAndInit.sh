#!/bin/bash

## check weblogic server is running

while :
do
    state=`java -classpath ${ORACLE_HOME}/wlserver_10.3/server/lib/weblogic.jar weblogic.Admin -url t3://${ADMINSERVER_URL} -username ${WLS_ADMIN} -password ${WLS_PASSWD} GETSTATE| cut -d\: -f2`
    if [[ "$state" == *RUNNING* ]];
    then
        break
    else
        sleep 5
    fi
done

echo "<-------------------------- WebLogic Server Running !! -------------------------->"
echo "<----- Create ManagedServer & DataSource & Application will be deployed --------->"

## create datasource & deploy application

if [ "${SERVER_TYPE}" == "adminserver" ]; then
  exec ${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh ${DOMAIN_HOME}/scripts/deploy_app.py
elif [ "${SERVER_TYPE}" == "managedserver" ]; then
  exec ${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh ${DOMAIN_HOME}/scripts/deploy_server.py
fi