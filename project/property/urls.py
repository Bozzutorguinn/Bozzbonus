from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^property', views.PropertyIndex, name='index')
]