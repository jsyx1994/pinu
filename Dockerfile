FROM index.tenxcloud.com/tenxcloud/ubuntu

MAINTAINER laowang
RUN apt-get update
RUN apt-get install -y python-pip 
RUN pip install uwsgi 
RUN pip install django==1.9.4
EXPOSE 80

VOLUME ["/pinu"]
