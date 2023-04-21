FROM centos:7

RUN yum -y install centos-release-scl epel-release
RUN yum -y install gcc libjpeg-turbo-devel make rh-python38 rh-python38-python-devel zlib-devel
RUN /opt/rh/rh-python38/root/usr/bin/pip install poetry

CMD ["scl", "enable", "rh-python38", "/bin/bash"]

