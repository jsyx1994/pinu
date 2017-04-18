from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^index/(?P<option>[^create,^myself].*)?$',views.list,name = 'index'),
        url(r'^myself/(?P<option>.*)?',views.myself,name = 'myself'),
        url(r'^create/$',views.create,name = 'create'),
        url(r'^(?P<activity_id>[0-9]+)/quit/$',views.quit,name = 'quit'),
        #url(r'^create/',views.create,name = 'create'),
        ]
