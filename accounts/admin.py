from django.contrib import admin

from .models import User, RequestLog, ContentDevice, PrivateNotification
# Register your models here.


admin.site.register(User)
admin.site.register(RequestLog)
admin.site.register(ContentDevice)
admin.site.register(PrivateNotification)
