from django.db import models
from django.core.urlresolvers import reverse

# Import user model for relationships
# from django.contrib.auth.models import User

class Business(models.Model):
    user            = models.ForeignKey(User)
    name            = models.CharField(max_length=100)
    phone           = models.IntegerField()
    website         = models.CharField(max_length=255, null=True, blank=True)
    address_street1 = models.CharField(max_length=100)
    address_street2 = models.CharField(max_length=100, null=True, blank=True)
    address_city    = models.CharField(max_length=100)
    address_state   = models.CharField(max_length=2)
    address_zip     = models.IntegerField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('business_detail', kwargs={'pk': self.pk})

class Review(models.Model):
    business        = models.ForeignKey('Business')
    rating          = models.IntegerField()
    subject         = models.CharField(max_length=100)
    body            = models.TextField()

    def __unicode__(self):
        return self.subject

class Category(models.Model):
    name = models.CharField(max_length=100)
    business = models.ManyToManyField(Business)

    def __unicode__(self):
        return self.name


