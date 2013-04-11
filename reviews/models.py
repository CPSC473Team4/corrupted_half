from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import phonenumbers

# Import user model for relationships
# from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

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
    address_lat     = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    address_lon     = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    category        = models.ManyToManyField(Category)
    photo           = ImageField(upload_to='photos/%Y/%m')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('business_detail', kwargs={'pk': self.pk})

    def formatted_phone(self, country=None):
        phone_number = phonenumbers.parse(self.phone, "US")
        print phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)

    def address_string(self):
        if self.address_street2:
            street_address = self.address_street1 + ' ' + self.address_street2
        else:
            street_address = self.address_street1

        return street_address + ', ' + self.address_city + ', ' + self.address_state + ' ' + str(self.address_zip)

    def get_avg_rating(self):
        reviews = Review.objects.filter(business__pk= self.pk)
        reviews_count = reviews.count()

        total_rating = 0
        for review in reviews:
            total_rating += review.rating

        return total_rating / reviews_count if reviews_count > 0 else 0


class Review(models.Model):
    business        = models.ForeignKey('Business')
    rating          = models.IntegerField()
    subject         = models.CharField(max_length=100)
    body            = models.TextField()

    def __unicode__(self):
        return self.subject
