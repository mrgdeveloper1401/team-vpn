from django.contrib import admin

from .models import Plan, Country, Domain, Config
# Register your models here.


admin.site.register(Plan)
admin.site.register(Country)
admin.site.register(Domain)
admin.site.register(Config)
