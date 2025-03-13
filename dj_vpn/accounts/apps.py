from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dj_vpn.accounts'

    def ready(self):
        import dj_vpn.accounts.signals
