## Install Oracle WebLogic 11g
## 2017.07.10 by Yun Insu ora01000@time-gate.com

FROM centos:centos6

MAINTAINER ora01000@time-gate.com


ENV SERVER_TYPE=adminserver \
	ADMINSERVER_URL=localhost:7001 \
	JAVA_HOME=/oracle/jdk1.7.0_80 \
	JAVA_VERSION=1.7.0_80 \
	JAVA_VENDOR=oracle \
	ORACLE_HOME=/oracle/middleware \
	DOMAIN_HOME=/oracle/domains/base_domain \
	LOG_HOME=/oracle/logs \
	WLS_ADMIN=weblogic \
	WLS_PASSWD=weblogic123 \
	MIN_HEAP=1024 \
	MAX_HEAP=1024 \
	MIN_PERM=512 \
	MAX_PERM=512 \
	MIN_NEW=384 \
	MAX_NEW=384 \
	SURVIVOR_RATIO=9 \
	ADDITIONAL_JAVA_OPTIONS= \
	MIN_POOL_SIZE=50
	
ENV	PATH=${JAVA_HOME}/bin:${ORACLE_HOME}/maven/bin:/$PATH \
	HOME=/home/weblogic
ENV WEBLOGIC_IMAGE_NAME="ora01000/weblogic-cluster" \
    WEBLOGIC_IMAGE_VERSION="10.3.6" \
    WEBLOGIC_IMAGE_RELEASE="1" \
    STI_BUILDER="jee"
    
# Labels
LABEL name="$WEBLOGIC_IMAGE_NAME" \
      version="$WEBLOGIC_IMAGE_VERSION" \
      release="$WEBLOGIC_IMAGE_RELEASE" \
      architecture="x86_64" \
      com.redhat.component="oracle-weblogic-11g-docker" \
      io.k8s.description="Platform for building and running JavaEE applications on Oracle WebLogicServer 11g Cluster" \
      io.k8s.display-name="Oracle WebLogicServer 11g cluster" \
      io.openshift.expose-services="7001:http" \
      io.openshift.tags="builder,javaee,weblogic,weblogic11g,cluster" \
      io.openshift.s2i.scripts-url="image:///usr/local/s2i"
		
USER 0

# yum install
RUN yum -y install wget net-tools bash-completion httpd-tools && \
	yum clean all && \
	groupadd -g 1001 -r weblogic && useradd -u 1001 -r -m -g weblogic weblogic -p 'weblogic' -d ${HOME}


RUN mkdir -p ${ORACLE_HOME} && mkdir -p ${JAVA_HOME} && mkdir -p ${LOG_HOME} && \
	mkdir -p /oracle/domains && mkdir -p ${HOME}/.m2 && chmod 777 ${LOG_HOME} && chmod -R 777 ${HOME} && \
	mkdir -p ${HOME}/deployments && chmod 777 ${HOME}/deployments
	
COPY settings.xml ${HOME}/.m2

COPY jdk1.7.0_80 /oracle/jdk1.7.0_80
COPY middleware /oracle/middleware
COPY domains /oracle/domains
COPY container-scripts/scripts /oracle/domains/base_domain/scripts
COPY container-scripts/startA.sh /oracle/domains/base_domain
COPY container-scripts/startWebLogic.sh /oracle/domains/base_domain
COPY usr/local/s2i /usr/local/s2i

RUN chown -R weblogic.weblogic /oracle && chown -R weblogic.weblogic ${HOME}/.m2

USER 1001

EXPOSE 7001

CMD ["/oracle/domains/base_domain/startA.sh"]
