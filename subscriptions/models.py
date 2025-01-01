from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class UserConfig(CreateMixin, UpdateMixin, SoftDeleteMixin):
    user = models.ForeignKey("accounts.User", on_delete=models.DO_NOTHING, related_name="user_subscription")
    config = models.ForeignKey('configs.Config', on_delete=models.DO_NOTHING, related_name="config_subscription")
    volume_usage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    volume = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.volume_usage} {self.is_active}'

    class Meta:
        db_table = "subscriptions"


# class Discount(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     config = models.ForeignKey("configs.Config", on_delete=models.DO_NOTHING, limit_choices_to={"is_free": False})
#     is_percent = models.BooleanField(default=False)
#     is_value = models.BooleanField(default=False)
#     amount = models.FloatField(default=1, validators=[MinValueValidator(1)])
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f'{self.is_percent} {self.amount}'
#
#     def clean(self):
#         if self.is_percent and self.is_value:
#             raise ValidationError({"is_value": _("is value and is percent both not choices")})
#         if not self.is_percent and not self.is_value:
#             raise ValidationError({"is_percent": _("You must choose one of the percentage and value fields")})
#         exiting_discount = Discount.objects.filter(config=self.config, is_active=True).exclude(pk=self.pk)
#         if exiting_discount.exists():
#             raise ValidationError({"config", "discount already exists"})
#
#     @property
#     def calc_config_price(self):
#         price = self.config.price
#         if self.is_value:
#             price = price - self.amount
#         if self.is_percent:
#             price = (price * self.amount) / 100
#         return max(price, 0)
#
#     class Meta:
#         db_table = "discounts"
#
#
# class Coupon(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     coupon_code = models.CharField(max_length=50, unique=True)
#     max_used = models.PositiveIntegerField(validators=[MinValueValidator(1)],
#                                            help_text=_("چند نفر میتوانند از این کد تخفیف استفاده کنند"))
#     number_of_used = models.PositiveIntegerField(default=0,
#                                                  help_text=_("تعداد افراد استفاده از این کد تخفیف"))
#     expired_date = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     coupon_type = models.CharField(_("نوع کد تخفیف"),
#                                    choices=(("is_percent", "درصد"), ("is_value", "مقدار")))
#     coupon_price = models.FloatField(_("مقدار کد تخفیف"), validators=[MinValueValidator(1)])
#     min_value = models.FloatField(_("حداقل قیمت"), blank=True, null=True,
#                                   help_text=_("این فیلد میتوانید مشخص کنید که هر خرید حداقل چه چقدر باشه که "
#                                               "بتوان از این کد تخفیف استفاده کرد"))
#     max_value = models.FloatField(_("حداکثر قیمت"), help_text=_("در این فیلد میتوان مشخص کرد که حداکثر تخفیف به این"
#                                                       "کد چقدر باشه"),
#                                   blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.coupon_code} {self.max_used} {self.number_of_used}'
#
#     class Meta:
#         db_table = "coupons"
