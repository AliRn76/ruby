from django.apps import AppConfig


class PvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pv'

    def ready(self):
        import pv.signals
