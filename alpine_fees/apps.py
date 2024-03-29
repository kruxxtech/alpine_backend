from django.apps import AppConfig


class AlpineFeesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alpine_fees"

    def ready(self):
        import alpine_fees.signals
