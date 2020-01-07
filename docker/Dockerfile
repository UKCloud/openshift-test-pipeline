FROM registry.access.redhat.com/openshift3/jenkins-slave-base-rhel7:latest

USER root

RUN yum-config-manager --enable rhel-7-server-rpms > /dev/null --enable rhel-7-server-extras-rpms > /dev/null

# Install ansible and prerequisites.
RUN yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y
RUN yum install python-devel gcc ansible wget glibc jq -y

# Install OC client.
RUN wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz \
    && tar -xvzf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz \
    && cd openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit \
    && export PATH='$(pwd)':$PATH

USER 1001