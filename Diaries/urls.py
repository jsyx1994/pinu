from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',views.index,name = 'index'),
        url(r'^(?P<act_id>[0-9]+)/edit/$',views.edit,name = 'edit'),
        url(r'^myself/$',views.myself,name = 'myself'),
        url(r'^(?P<dia_id>[0-9]+)/detail/$',views.detail,name = 'detail'),
        url(r'^(?P<dia_id>[0-9]+)/alter/$',views.alter,name = 'alter'),
        ]
        