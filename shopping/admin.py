from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(product)
admin.site.register(user_detail)
admin.site.register(Cart)
admin.site.register(order_product)
admin.site.register(order_product_detail)