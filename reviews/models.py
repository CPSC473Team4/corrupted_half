# Both packages import "models" so we need to alias them
from django.contrib.gis.db import models as geoModels
from django.db import models as djangoModels

# Import user model for relationships
from django.contrib.auth.models import User

class Business(geoModels.Model):
	user            = geoModels.ForeignKey(User)
	name            = geoModels.CharField(max_length=100)
	phone           = geoModels.IntegerField()
	website         = geoModels.CharField(max_length=255)
	address_street1 = geoModels.CharField(max_length=100)
	address_street2 = geoModels.CharField(max_length=100)
	address_city    = geoModels.CharField(max_length=100)
	address_state   = geoModels.CharField(max_length=2)
	address_zip     = geoModels.IntegerField()
	lon             = geoModels.FloatField()
	lat             = geoModels.FloatField()


class Category(djangoModels.Model):
	name = djangoModels.CharField(max_length=100)

class Business_Category(djangoModels.Model):
	business = djangoModels.ForeignKey(Business)
	category = djangoModels.ForeignKey(Category)

class Review(djangoModels.Model):
	business = djangoModels.ForeignKey(Business)
	user = djangoModels.ForeignKey(User)