from django.contrib import admin

from .models import Images
# Register your models here.


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image_size', "image_width", "image_height", "created_at"]
