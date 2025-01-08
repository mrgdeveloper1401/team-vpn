from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# from configs.enums import ProtocolChoices
from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Country(CreateMixin, UpdateMixin, SoftDeleteMixin):
    country_name = models.CharField(max_length=255, db_index=True,
                                    help_text=_("Names of countries in English"))
    ir_country_name = models.CharField(max_length=255, blank=True, null=True,
                                       help_text=_("نام کشورها به صورت فارسی"))
    # country_image = models.ForeignKey("cores.Images", on_delete=models.DO_NOTHING, related_name="country_image",
    #                                   blank=True, null=True, help_text=_("عکس کشور"))
    country_code = models.CharField(max_length=255, help_text=_("کد کشور"))
    is_active = models.BooleanField(default=True, help_text=_("قابل نمایش"))

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = "country"


class Config(CreateMixin, UpdateMixin, SoftDeleteMixin):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name="country_configs",
                                help_text=_("کشور مورد نظر"))
    config = models.TextField(help_text=_("کانفینگ"))
    # protocol = models.CharField(choices=ProtocolChoices.choices,
    #                             help_text=_("پروتوکول های فیلترشکن"))
    is_free = models.BooleanField(default=False, help_text=_("رایگان"))
    is_active = models.BooleanField(default=True, help_text=_("قابل نمایش"))
    price = models.FloatField(blank=True, null=True, help_text=_("قیمت کانفیگ"))
    # volume = models.PositiveIntegerField(help_text=_("حجم کانفینگ"))

    def __str__(self):
        return self.config

    def clean(self):
        if self.is_free and self.price:
            raise ValidationError({"price": _("is free and price both not choices")})
        if not self.is_free and not self.price:
            raise ValidationError({"price": _("You have to choose between free and price")})

    class Meta:
        db_table = "config"


# class Domain(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     domain = models.CharField(max_length=255, db_index=True, help_text=_("نام دامنه"))
#     is_blocked = models.BooleanField(default=False, help_text=_("بلاک بودن دامنه"))
#     is_active = models.BooleanField(default=True, help_text=_("قابل نمایش"))
#
#     def __str__(self):
#         return self.domain
#
#     class Meta:
#         db_table = 'domain'
