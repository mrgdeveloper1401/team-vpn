from django.db import models


class AccountType(models.TextChoices):
    normal_user = "normal_user"
    premium_user = "premium_user"


class AccountStatus(models.TextChoices):
    LIMIT = "limit"
    EXPIRED = "expired"
    BEN = "ben"
    NOTHING = "nothing"
