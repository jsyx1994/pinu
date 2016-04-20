FROM ubuntu:14.04

MAINTAINER laowang
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y nginx

RUN apt-get install -y python-pip 
RUN pip install uwsgi 
RUN pip install django==1.9.4
RUN apt-get install -y openssh-server
RUN RUN mkdir /var/run/sshd
RUN echo "root:123456" | chpasswd

VOLUME ["/pinu"]
