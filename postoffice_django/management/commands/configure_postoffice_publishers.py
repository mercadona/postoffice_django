from django.core.management.base import BaseCommand

from ...config import configure_publishers


class Command(BaseCommand):
    help = 'Create all publishers to can consume messages via postoffice'

    def handle(self, *args, **kwargs):
        configure_publishers()
