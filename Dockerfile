FROM index.tenxcloud.com/tenxcloud/ubuntu

MAINTAINER laowang
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN apt-get install -y vim
RUN pip install uwsgi 
RUN pip install django==1.9.4
RUN pip install Pillow==2.3.0

RUN apt-get install -y nginx

RUN rm /etc/nginx/sites-enabled/default
ADD origin2_0.conf /etc/nginx/sites-enabled/
VOLUME ["/pinu"]
EXPOSE 80
