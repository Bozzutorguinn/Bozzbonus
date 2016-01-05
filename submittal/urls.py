from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<submittal_id>[0-9]+)/$', views.SubmittalDetail, name='submittal_detail')
]