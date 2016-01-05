from __future__ import unicode_literals
from django.db import models

#this class is used to store all of the employees available to be selected from HR
#there is no assignment to specific properties and/or submittals for bonus purposes in this class
#reference the submittal_employees class for assignments
class Employees(models.Model):
    emp_name_first = models.CharField(max_length=100, default='none')
    emp_name_last = models.CharField(max_length=100, default='none')
    emp_id = models.CharField(max_length=50, default='none')
    job_title = models.CharField(max_length=100, default='none')
    assigned_property = models.CharField(max_length=100, default='none')
    emp_status = models.CharField(max_length=100, default='none')
