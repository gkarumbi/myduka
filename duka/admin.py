from django.contrib import admin


# Register your models here.

from .models import Categories,Product,OrderItem,Order

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)

