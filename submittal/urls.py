from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<submittal_id>[0-9]+)/edit_opening_date/$', views.EditOpeningDate, name='edit_opening_date'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_stabilization_date/$', views.EditStabilizationDate, name='edit_stabilization_date'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_leasing_status/$', views.EditLeasingStatus, name='edit_leasing_status'),
    url(r'^(?P<submittal_id>[0-9]+)/$', views.SubmittalDetail, name='submittal_detail')
]