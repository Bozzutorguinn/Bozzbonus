from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<submittal_id>[0-9]+)/edit_yes_no/(?P<yes_no_type>\w+)/$', views.EditYesNo, name='edit_yes_no'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_quantity/(?P<quantity_input_type>\w+)/$', views.EditQuantityAmount, name='edit_quantity_amount'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_amount/(?P<dollar_input_type>\w+)/$', views.EditDollarAmount, name='edit_dollar_amount'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_rate/(?P<rate_type>\w+)/$', views.EditRate, name='edit_rate'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_opening_date/$', views.EditOpeningDate, name='edit_opening_date'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_stabilization_date/$', views.EditStabilizationDate, name='edit_stabilization_date'),
    url(r'^(?P<submittal_id>[0-9]+)/edit_leasing_status/$', views.EditLeasingStatus, name='edit_leasing_status'),
    url(r'^(?P<submittal_id>[0-9]+)/$', views.SubmittalDetail, name='submittal_detail')
]