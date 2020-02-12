from django.core.management.base import BaseCommand

from ...config import configure_topics


class Command(BaseCommand):
    help = 'Create all topics to be able to publish messages to postoffice'

    def handle(self, *args, **kwargs):
        configure_topics()
