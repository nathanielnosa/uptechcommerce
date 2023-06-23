from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)