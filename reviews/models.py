from django.contrib.gis.db import models

class Business(models.Model):
    name            = models.CharField(max_length=100)
    phone           = models.IntegerField()
    website         = models.CharField(max_length=255)
    address_street1 = models.CharField(max_length=100)
    address_street2 = models.CharField(max_length=100)
    address_city    = models.CharField(max_length=100)
    address_state   = models.CharField(max_length=2)
    address_zip     = models.IntegerField()
    lon             = models.FloatField()
    lat             = models.FloatField()

