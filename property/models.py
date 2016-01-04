from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Property(models.Model):
    prop_name = models.CharField(max_length=100)
    pm_user = models.ForeignKey(User, related_name='property_pm', default=0)
    rm_user = models.ForeignKey(User, related_name='property_rm', default=0)
    unit_count = models.IntegerField(default=0)

