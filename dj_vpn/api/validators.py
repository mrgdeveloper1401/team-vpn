from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from accounts.enums import AccountStatus, VolumeChoices, AccountType


class NumericValidator(RegexValidator):
    regex = r'\d'
    message = _("you must enter a numeric value")


def calc_volume_usage(user):
    result = False

    if user.accounts_status == AccountStatus.ACTIVE:

        if user.volume_choice == VolumeChoices.GB:
            if user.volume_usage / 1_000 > user.volume:
                user.account_type = AccountType.normal_user
                user.accounts_status = AccountStatus.LIMIT
            else:
                result = True

        if user.volume_choice == VolumeChoices.MG:
            if user.volume_usage > user.volume:
                user.account_type = AccountType.normal_user
                user.accounts_status = AccountStatus.LIMIT
            else:
                result = True

        if user.volume_choice == VolumeChoices.TRA:
            if user.volume_usage / 1_000_000 > user.volume:
                user.account_type = AccountType.normal_user
                user.accounts_status = AccountStatus.LIMIT
            else:
                result = True

    else:
        result = False
    return result
