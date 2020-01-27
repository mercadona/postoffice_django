from django.core.management.base import BaseCommand

from ...config import configure


class Command(BaseCommand):
    help = 'Create all topics and publishers to can use post office'

    def handle(self, *args, **kwargs):
        configure()
