from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<submittal_id>[0-9]+)/remove_employee/(?P<employee_id>[0-9]+)/$', views.RemoveEmployee, name='remove_employee'),
    url(r'^(?P<submittal_id>[0-9]+)/$', views.EditEmployees, name='edit_employees')
]