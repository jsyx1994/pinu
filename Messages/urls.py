from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^index/(?P<option>.*)?',views.list,name = 'index'),
        #url(r'^(?P<msg_id>[0-9]+)/detail/$',views.detail,name = 'detail'),
        url(r'^(?P<msg_id>[0-9]+)/delete/$',views.delete,name = 'delete'),
        ]
