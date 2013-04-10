from django.contrib import admin
from reviews.models import Business, Category, Review
from reviews.models import Business
from sorl.thumbnail.admin import AdminImageMixin

admin.site.register(Business)
admin.site.register(Category)
admin.site.register(Review)

class BusinessAdmin(AdminImageMixin, admin.ModelAdmin):
    pass

