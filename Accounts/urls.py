from django.conf.urls import url
from . import views

urlpatterns = [
	#url(r'^$',views.index,name ='index' ),
	url(r'^register/$',views.register,name = 'register'),
	url(r'^login/$',views.log_in,name = 'login'),
        url(r'^user_info/(img)?$',views.user_info,name = 'user_info'),
        url(r'^info_edit/$',views.info_edit,name = 'info_edit'),
        url(r'^logout/$',views.log_out,name = 'logout'),
        url(r'^friends/(?P<fri_id>[0-9]+)/$',views.fri_detail,name = 'fri_detail'),
        #url(r'^friends/list',views.list,name = ''),
]
