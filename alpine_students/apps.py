from django.apps import AppConfig


class AlpineStudentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alpine_students"

    def ready(self):
        import alpine_students.signals
