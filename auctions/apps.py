from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class AuctionsConfig(AppConfig):
    name = 'auctions'

    def ready(self):
        import auctions.signals  # noqa