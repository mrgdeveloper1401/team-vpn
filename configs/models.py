from django.db import models

from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Plan(CreateMixin, UpdateMixin, SoftDeleteMixin):
    plan_name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    volume = models.PositiveIntegerField()
    price = models.FloatField()
    image = models.ForeignKey("cores.Images", on_delete=models.DO_NOTHING, related_name="plan_image")
    description = models.TextField(null=True, blank=True)
    max_connect_device = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_name

    class Meta:
        db_table = "plan"


class Country(CreateMixin, UpdateMixin, SoftDeleteMixin):
    country_name = models.CharField(max_length=255)
    ir_country_name = models.CharField(max_length=255)
    country_image = models.ForeignKey("cores.Images", on_delete=models.DO_NOTHING, related_name="country_image",
                                      blank=True, null=True)

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = "country"


class Config(CreateMixin, UpdateMixin, SoftDeleteMixin):
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, related_name="plan_configs")
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name="country_configs")
    is_free = models.BooleanField(default=False)
    config = models.TextField()

    class Meta:
        db_table = "config"


class Domain(CreateMixin, UpdateMixin, SoftDeleteMixin):
    domain = models.CharField(max_length=255)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.domain

    class Meta:
        db_table = 'domain'
