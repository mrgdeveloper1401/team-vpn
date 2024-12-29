from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Subscription(CreateMixin, UpdateMixin, SoftDeleteMixin):
    user = models.ForeignKey("accounts.User", on_delete=models.DO_NOTHING, related_name="user_subscription")
    plan = models.ForeignKey("configs.Plan", on_delete=models.DO_NOTHING, related_name="plan_subscription")
    config = models.ForeignKey('configs.Config', on_delete=models.DO_NOTHING, related_name="config_subscription")
    volume_usage = models.PositiveIntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.volume_usage} {self.is_active}'

    class Meta:
        db_table = "subscriptions"


class Discount(CreateMixin, UpdateMixin, SoftDeleteMixin):
    plan = models.ForeignKey("configs.Plan", on_delete=models.CASCADE)
    is_percent = models.BooleanField(default=False)
    is_value = models.BooleanField(default=False)
    amount = models.FloatField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.is_percent} {self.amount}'

    def clean(self):
        if self.is_percent and self.is_value:
            raise ValidationError({"is_value": _("is value and is percent both not choices")})

    @property
    def calc_final_plan_price(self):
        price = self.plan.price
        if self.is_percent:
            price = (self.plan.price * self.amount) / 100
        if self.is_value:
            price = self.plan.price - self.amount
        return max(price, 0)

    class Meta:
        db_table = "discounts"


class Coupon(CreateMixin, UpdateMixin, SoftDeleteMixin):
    coupon_code = models.CharField(max_length=50, unique=True)
    max_used = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    number_of_used = models.PositiveIntegerField(default=0)
    expired_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.coupon_code} {self.max_used} {self.number_of_used}'

    class Meta:
        db_table = "coupons"
