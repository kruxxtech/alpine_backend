from django.apps import AppConfig


class AlpineUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alpine_users"

    def ready(self):
        import alpine_users.signals
