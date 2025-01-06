from django.db import models


class AccountType(models.TextChoices):
    normal_user = "normal_user"
    premium_user = "premium_user"


class AccountStatus(models.TextChoices):
    ACTIVE = "active"
    LIMIT = "limit"
    EXPIRED = "expired"
    NOTHING = "nothing"


class VolumeChoices(models.TextChoices):
    # NOTHING = 'nothing'
    MG = 'mg'
    GB = "gb"
    TRA = 'tra'
