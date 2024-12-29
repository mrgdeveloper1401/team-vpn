from django.contrib import admin

from .models import Order
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', "plan", "is_paid", "order_number", "created_at", "updated_at"]
    list_filter = ['is_paid']
    list_select_related = ['user', "plan"]
    raw_id_fields = ['user', "plan"]
    search_fields = ['user__username', "plan__plan_name"]
