from django.contrib import admin

from .models import UserConfig
# Register your models here.


# @admin.register(Discount)
# class DiscountAdmin(admin.ModelAdmin):
#     list_display = ['config', "amount", "is_percent", "is_value", "is_active", "calc_config_price"]
#     list_select_related = ['config']
#     list_editable = ['is_percent', "is_value", "is_active"]
#     list_filter = ['is_percent', "is_value", "is_active"]
#     raw_id_fields = ['config']


@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    list_display = ['user', "config", "volume_usage", "is_active"]
    list_filter = ['is_active']
    list_editable = ['is_active']
    raw_id_fields = ['user', "config"]
    list_select_related = ["user", "config"]


# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#     list_display = ['coupon_code', "max_used", "number_of_used", "expired_date", "coupon_price",
#                     "min_value", "max_value", "is_active"]
#     search_fields = ["coupon_code"]
#     list_filter = ['is_active']
#     list_editable = ['is_active']
