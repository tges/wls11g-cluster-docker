#!/bin/bash
# process running
if [ "${SERVER_TYPE}" == "adminserver" ]; then
  SVR="AdminServer"
  
elif [ "${SERVER_TYPE}" == "managedserver" ]; then
  SVR=${HOSTNAME}
  
fi


# process running checking !!!
#PID=`ps -ef|grep java|grep ${SVR}|awk '{print $2}'`
#if [ "$PID" != "" ]
#then
# echo .
# echo "${SVR}"_[pid:"${PID}"] Process Is Running !!!
# echo .
#  exit
#fi

# Make boot.properties
echo "username=${WLS_ADMIN}" >> /oracle/domains/base_domain/boot.properties
echo "password=${WLS_PASSWD}" >> /oracle/domains/base_domain/boot.properties


USER_MEM_ARGS="-D${SVR} -Xms${MIN_HEAP}m -Xmx${MAX_HEAP}m -XX:NewSize=${MIN_NEW}M -XX:MaxNewSize=${MAX_NEW}M -XX:PermSize=${MIN_PERM}m -XX:MaxPermSize=${MAX_PERM}m -XX:SurvivorRatio=${SURVIVOR_RATIO} -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=15 -XX:ParallelGCThreads=8 -XX:+UseParallelOldGC -XX:-UseAdaptiveSizePolicy -XX:+DisableExplicitGC -Xloggc:/oracle/logs/gc.out"

export USER_MEM_ARGS
export JAVA_OPTIONS="${JAVA_OPTIONS} -Dweblogic.threadpool.MinPoolSize=${MIN_POOL_SIZE}"

## PostgreSQL JDBC
export PRE_CLASSPATH="${ORACLE_HOME}/wlserver_10.3/server/lib/postgresql-42.1.1.jre7.jar:${PRE_CLASSPATH}"


#mv ./logs/nohup.${SVR}.out ./logs/${SVR}/nohup.${SVR}_`date +'%Y%m%d_%H%M%S'`.out
#mv ./logs/gc.${SVR}.out ./logs/${SVR}/gc.${SVR}_`date +'%Y%m%d_%H%M%S'`.out

touch ${LOG_HOME}/nohup.out


if [ "${SERVER_TYPE}" == "adminserver" ]; then
  echo "===================> SERVER_TYPE = adminserver ==============" >> ${LOG_HOME}/nohup.out
  nohup ${DOMAIN_HOME}/bin/startWebLogic.sh >> ${LOG_HOME}/nohup.out 2>&1 &
  nohup ${DOMAIN_HOME}/scripts/checkAdminServerAndInit.sh >> ${LOG_HOME}/nohup.out &
  nohup ${DOMAIN_HOME}/scripts/checkDeletedManagedServer.sh >> ${LOG_HOME}/nohup.out &
  
elif [ "${SERVER_TYPE}" == "managedserver" ]; then
  echo "===================> SERVER_TYPE = managedserver ==============" >> ${LOG_HOME}/nohup.out
  export POD_IP=`ifconfig eth0 | grep 'inet addr' | cut -d\: -f2 | cut -d' ' -f1`
  echo "===================> POD_IP = ${POD_IP} ==================" >> ${LOG_HOME}/nohup.out
  
  ${DOMAIN_HOME}/scripts/checkAdminServerAndInit.sh >> ${LOG_HOME}/nohup.out
  nohup ${DOMAIN_HOME}/bin/startManagedWebLogic.sh ${HOSTNAME} t3://${ADMINSERVER_URL} >> ${LOG_HOME}/nohup.out 2>&1 &
  
fi


tail -f ${LOG_HOME}/nohup.out