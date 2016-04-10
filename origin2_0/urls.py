"""origin1_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from Accounts import views as lend_views
from django.views.static import serve
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',lend_views.index,name = 'index'),
    url(r'^accounts/',include('Accounts.urls',namespace = 'accounts')),
    url(r'^activities/',include('Activities.urls',namespace = 'activities')),
    url(r'^messages/',include('Messages.urls',namespace = 'messages')),
    ]
if settings.DEBUG:
    urlpatterns += (
            url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
            )
