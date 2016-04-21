FROM index.tenxcloud.com/tenxcloud/ubuntu

MAINTAINER laowang
RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN apt-get install -y vim
RUN pip install uwsgi 
RUN pip install django==1.9.4
RUN pip install Pillow==2.3.0
RUN pip install supervisor
RUN echo_supervisord_conf > /etc/supervisord.conf
RUN echo -e "[program:pinu]\ncommand=uwsgi --ini /pinu/pinu-master/uwsgi.ini\nstartsecs=0\nstopwaitsecs=0\nautostart=true\nautorestart=true" >> /etc/supervisord.conf
RUN supervisord -c /etc/supervisord.conf 
RUN supervisorctl reload
RUN supervisorctl -c /etc/supervisord.conf restart pinu
RUN apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default


#RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
ADD origin2_0.conf /etc/nginx/sites-enabled/

VOLUME ["/pinu"]
EXPOSE 80

#CMD ["/usr/sbin/nginx"]
RUN service nginx reload
RUN service nginx restart

#CMD ["uwsgi","--ini","/pinu/pinu-master/uwsgi.ini"]
