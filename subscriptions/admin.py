from django.contrib import admin

from .models import Discount, Coupon, Subscription
# Register your models here.


admin.site.register(Discount)
admin.site.register(Coupon)
admin.site.register(Subscription)
