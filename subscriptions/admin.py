from django.contrib import admin

from .models import Discount, Coupon, Subscription
# Register your models here.


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['plan', "amount", "is_percent", "is_value", "is_active", "calc_final_plan_price"]
    list_select_related = ['plan']
    list_editable = ['is_percent', "is_value", "is_active"]
    list_filter = ['is_percent', "is_value", "is_active"]
    raw_id_fields = ['plan']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', "plan", "config", "volume_usage", "is_active"]
    list_filter = ['is_active']
    list_editable = ['is_active']
    raw_id_fields = ['user', "plan", "config"]
    list_select_related = ['plan', "user", "config"]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', "max_used", "number_of_used", "expired_date", "is_active"]
    search_fields = ["coupon_code"]
    list_filter = ['is_active']
    list_editable = ['is_active']
