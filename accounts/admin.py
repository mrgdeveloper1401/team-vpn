from django.contrib import admin

from .models import User, RequestLog, ContentDevice, PrivateNotification
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    pass


admin.site.register(RequestLog)
admin.site.register(ContentDevice)
admin.site.register(PrivateNotification)
