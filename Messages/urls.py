from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$',views.list,name = 'list'),
        url(r'^(?P<msg_id>[0-9]+)/detail/$',views.detail,name = 'detail'),
        ]
