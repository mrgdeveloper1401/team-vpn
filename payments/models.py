from uuid import uuid4

from django.db import models

from cores.models import CreateMixin, UpdateMixin, SoftDeleteMixin


# class Order(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     user = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, related_name="user_order")
#     config = models.ForeignKey('configs.Config', on_delete=models.DO_NOTHING, related_name="config_order")
#     is_paid = models.BooleanField(default=False)
#     order_number = models.CharField(max_length=255, unique=True)
#     price = models.FloatField()
#
#     @property
#     def generate_order_number(self):
#         order_number = str(uuid4().hex)[:10]
#         return order_number
#
#     def save(self, *args, **kwargs):
#         if not self.order_number:
#             self.order_number = self.generate_order_number
#         return super().save(*args, **kwargs)
#
#     class Meta:
#         db_table = 'order'


# class Transaction(CreateMixin, UpdateMixin, SoftDeleteMixin):
#     pass

