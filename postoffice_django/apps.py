from django.apps import AppConfig


class PostofficeDjangoConfig(AppConfig):
    name = 'postoffice_django'

    def ready(self):
        from .publishing import publish  # noqa
