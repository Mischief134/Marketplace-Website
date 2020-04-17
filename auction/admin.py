from django.contrib import admin

# Register your models here.
from auction.models import *

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(ProductRating)
admin.site.register(Cart)
admin.site.register(Order)
