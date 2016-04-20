FROM ubuntu:14.04

MAINTAINER laowang
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y nginx

RUN apt-get install -y python-pip 
RUN pip install uwsgi 
RUN pip install django==1.9.4
RUN apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd && sed -i "s/UsePrivilegeSeparation./UsePrivilegeSeparation no/g" /etc/ssh/sshd_config && sed -i "s/UsePAM./UsePAM no/g" /etc/ssh/sshd_config && sed -i "s/PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config
EXPOSE 80 22

VOLUME ["/pinu"]
CMD /usr/sbin/nginx
