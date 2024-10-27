from django.apps import AppConfig


class DecksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "decks"

    # active singnal for decks Model:
    def ready(self):
        import decks.signals
