FROM index.tenxcloud.com/tenxcloud/ubuntu

MAINTAINER laowang
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN apt-get install -y vim
RUN pip install uwsgi 
RUN pip install django==1.9.4
RUN apt-get install -y nginx

#RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
#ADD sites-enabled/ /etc/nginx/sites-enabled/
VOLUME ["/pinu"]
ADD ./* /pinu/
EXPOSE 80

#CMD ["/usr/sbin/nginx"]
