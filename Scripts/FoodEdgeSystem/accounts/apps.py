from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals