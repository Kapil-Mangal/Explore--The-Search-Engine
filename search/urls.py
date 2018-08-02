from django.conf.urls import url
from . import views

app_name='search'
urlpatterns=[
    # /
    url(r'^$', views.index, name='index'),
    url(r'^searching/$',views.detail,name='detail'),
    url(r'^searching/(?P<r>[a-zA-Z0-9_]+.txt)/$',views.favorite,name='favorite'),
    ]
