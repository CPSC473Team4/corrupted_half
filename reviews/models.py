from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import phonenumbers
from geopy import geocoders

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
    description     = models.TextField(null=True, blank=True)
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
        phone_number = phonenumbers.parse(str(self.phone), "US")
        print phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)

    def address_string(self):
        return self.formatted_address(' ')

    def address_html(self):
        return self.formatted_address('<br />')

    def formatted_address(self, separator):
        if self.address_street2:
            street_address = self.address_street1 + ' ' + self.address_street2
        else:
            street_address = self.address_street1

        return street_address + separator + self.address_city + ', ' + self.address_state + ' ' + str(self.address_zip)

    def get_avg_rating(self):
        reviews = Review.objects.filter(business__pk= self.pk)
        reviews_count = reviews.count()

        total_rating = 0
        for review in reviews:
            total_rating += review.rating

        return total_rating / reviews_count if reviews_count > 0 else 0

    @staticmethod
    def search(latitude, longitude, radius, category='', max_results=25, use_miles=True):

        distance_unit = 3959 if use_miles else 6371

        from django.db import connection, transaction
        import math

        cursor = connection.cursor()

        connection.connection.create_function('acos', 1, math.acos)
        connection.connection.create_function('cos', 1, math.cos)
        connection.connection.create_function('radians', 1, math.radians)
        connection.connection.create_function('sin', 1, math.sin)

        sql = """SELECT reviews_business.*, (%s * acos( cos( radians(%s) ) * cos( radians( address_lat ) ) *
            cos( radians( address_lon ) - radians(%s) ) + sin( radians(%s) ) * sin( radians( address_lat ) ) ) )
            AS distance FROM reviews_business """

        params = [distance_unit, latitude, longitude, latitude]

        if category:
            sql += """JOIN reviews_business_category ON reviews_business.id = reviews_business_category.business_id
                      JOIN reviews_category ON reviews_business_category.category_id = reviews_category.id"""

        sql += " WHERE distance < %s"
        params.append(int(radius))

        if category:
            sql += " AND reviews_category.slug = %s"
            params.append(category)

        sql += " ORDER BY distance;"

        return Business.objects.raw(sql, params)

    def save(self, *args, **kwargs):
        try:
            geocoder = geocoders.GoogleV3()
            place, (lat, lon) = geocoder.geocode(self.address_string(), exactly_one=False)[0]

            # Assign the geocoded latitude & longitude
            self.address_lat = lat
            self.address_lon = lon
        except:
            pass

        super(Business, self).save(*args, **kwargs)


class Review(models.Model):
    business        = models.ForeignKey('Business')
    rating          = models.IntegerField()
    subject         = models.CharField(max_length=100)
    body            = models.TextField()

    def __unicode__(self):
        return self.subject
