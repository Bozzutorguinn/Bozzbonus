from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Property(models.Model):
    prop_name = models.CharField(max_length=100)
    pm_user = models.ForeignKey(User, related_name='property_pm', default=0)
    rm_user = models.ForeignKey(User, related_name='property_rm', default=0)
    unit_count = models.IntegerField(default=0)
    prop_number_yardi = models.CharField(max_length=12, default='0')
    prop_number_jde = models.CharField(max_length=12, default='0')
    #based on the first month of the property's fiscal year which is used in calculating bonus amounts
    #options are 1-12 corresponding to the months of the year
    #defaults to January (1)
    fiscal_start = models.IntegerField(default=1)
    date_opening = models.DateField(null=True)
    date_stabilization = models.DateField(null=True)


