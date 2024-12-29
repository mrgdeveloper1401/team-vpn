from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Plan(CreateMixin, UpdateMixin, SoftDeleteMixin):
    plan_name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    volume = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField(validators=[MinValueValidator(1)])
    image = models.ForeignKey("cores.Images", on_delete=models.DO_NOTHING, related_name="plan_image")
    description = models.TextField(null=True, blank=True)
    max_connect_device = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_name

    class Meta:
        db_table = "plan"


class Country(CreateMixin, UpdateMixin, SoftDeleteMixin):
    country_name = models.CharField(max_length=255, db_index=True,
                                    help_text=_("Names of countries in English"))
    ir_country_name = models.CharField(max_length=255, db_index=True,
                                       help_text=_("نام کشورها به صورت فارسی"))
    country_image = models.ForeignKey("cores.Images", on_delete=models.DO_NOTHING, related_name="country_image",
                                      blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = "country"


class Config(CreateMixin, UpdateMixin, SoftDeleteMixin):
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, related_name="plan_configs")
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name="country_configs")
    is_free = models.BooleanField(default=False)
    config = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "config"


class Domain(CreateMixin, UpdateMixin, SoftDeleteMixin):
    domain = models.CharField(max_length=255, db_index=True)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.domain

    class Meta:
        db_table = 'domain'
