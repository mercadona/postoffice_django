from django.core.management.base import BaseCommand

from ...config import configure_publishers, configure_topics


class Command(BaseCommand):
    help = 'Configure both topics and publishers on PostOffice'

    def handle(self, *args, **kwargs):
        configure_topics()
        configure_publishers()
