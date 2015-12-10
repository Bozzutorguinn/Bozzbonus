from __future__ import unicode_literals

from django.db import models

class Property(models.Model):
    prop_name = models.CharField(max_length=100)


