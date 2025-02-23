from django.db import models
from django.utils.translation import gettext_lazy as _

from dj_vpn.cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Country(CreateMixin, UpdateMixin, SoftDeleteMixin):
    en_country_name = models.CharField(max_length=255, db_index=True,
                                       help_text=_("Names of countries in English"))
    fa_country_name = models.CharField(max_length=255, blank=True, null=True,
                                       help_text=_("نام کشورها به صورت فارسی"))
    country_code = models.CharField(max_length=255, help_text=_("کد کشور"))

    def __str__(self):
        return self.en_country_name

    class Meta:
        db_table = "country"


class Config(CreateMixin, UpdateMixin, SoftDeleteMixin):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name="country_configs",
                                help_text=_("کشور مورد نظر"))
    config = models.TextField(help_text=_("کانفینگ"))
    config_type = models.CharField(choices=[("tunnel_server", _("سرور تانل")), ("direct_server", _("سرور مستقیم"))],
                                   max_length=14, blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text=_("قابل نمایش"))

    def __str__(self):
        return self.config

    class Meta:
        db_table = "config"
        ordering = ('-created_at',)
