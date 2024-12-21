from django.db import models


from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class Subscription(CreateMixin, UpdateMixin, SoftDeleteMixin):
    user = models.ForeignKey("accounts.User", on_delete=models.DO_NOTHING, related_name="user_subscription")
    plan = models.ForeignKey("configs.Plan", on_delete=models.DO_NOTHING, related_name="plan_subscription")
    volume_usage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.volume_usage} {self.is_active}'

    class Meta:
        db_table = "subscriptions"


class Discount(CreateMixin, UpdateMixin, SoftDeleteMixin):
    plan = models.ForeignKey("configs.Plan", on_delete=models.CASCADE)
    is_percent = models.BooleanField(default=False)
    is_value = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.is_percent} {self.amount}'

    class Meta:
        db_table = "discounts"


class Coupon(CreateMixin, UpdateMixin, SoftDeleteMixin):
    coupon_code = models.CharField(max_length=50, unique=True)
    max_used = models.PositiveIntegerField()
    number_of_used = models.PositiveIntegerField(default=0)
    expired_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.coupon_code} {self.max_used} {self.number_of_used}'

    class Meta:
        db_table = "coupons"
