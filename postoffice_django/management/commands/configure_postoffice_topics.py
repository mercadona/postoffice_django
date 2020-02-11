from django.core.management.base import BaseCommand

from ...config import configure_topics


class Command(BaseCommand):
    help = 'Create all topics to can publish messages to post office'

    def handle(self, *args, **kwargs):
        configure_topics()
