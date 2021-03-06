from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^property_test/$', views.PropertyTest, name='property_test'),
    url(r'^(?P<property_id>[0-9]+)/$', views.PropertyDetail, name='property_detail'),
    url(r'^', views.PropertyIndex, name='index'),
]