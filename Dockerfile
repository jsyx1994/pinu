FROM ubuntu:14.04

MAINTAINER laowang
RUN echo "deb http://archive.ubuntu.com/ubuntu/ raring main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

RUN apt-get install python-pip 
RUN pip install uwsgi 
RUN pip install django==1.9.4

VOLUME ["/pinu"]
CMD /usr/sbin/nginx
