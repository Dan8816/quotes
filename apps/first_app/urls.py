from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^myaccount/(?P<user_id>\d+)$', views.myaccount),
    url(r'^update$', views.update),
    url(r'^success/post_quote$', views.create_quote),
    url(r'^(?P<id>\d+)/del_quote$', views.del_quote),
    url(r'^user/(?P<user_id>\d+)$', views.thisUserQuotes),
    url(r'^(?P<id>\d+)/like$', views.like),
]