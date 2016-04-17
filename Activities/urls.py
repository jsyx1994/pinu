from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^(?P<option>[^create,^myself].*)?$',views.list,name = 'index'),
        url(r'^myself',views.myself,name = 'myself'),
        url(r'^create/$',views.create,name = 'create'),
        url(r'^(?P<activity_id>[0-9]+)/detail/$',views.detail,name = 'detail'),
        #url(r'^create/',views.create,name = 'create'),
        ]
