from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$',index_views),
    url(r'^login/$',login_views),
    url(r'^register/$',register_views),
    url(r'^check_uphone/$',check_uphone_views),
    url(r'^check_login/$',check_login_views),
    url(r'^logout/$',logout_views),
    url(r'^get_stores',get_stores_views),
    url(r'^cart/$',cart_views),
    # url(r'^get_windows',get_windows_views),
    url(r'^balance/$',balance_views),
    url(r'^pay_for/$',pay_for_views),
]