from __future__ import unicode_literals
from submittal.models import Submittal
from employees.models import Employees
from django.db import models

class Submittal_Employees(models.Model):
    submittal = models.ForeignKey(Submittal)
    #referenced the user ID from the Employees application
    employee = models.ForeignKey(Employees)
    #sets the allocation rate of the total renewal bonus between each of the employees
    #total should always equal 100%
    renewal_sharing_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #reference for the number of failed shops that the employee incurs for purposes of deducting bonus
    failed_shops = models.IntegerField(default=0)
