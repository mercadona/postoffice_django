from django.core.management.base import BaseCommand

from ...config import configure_publishers


class Command(BaseCommand):
    help = 'Create publishers to be able to consume messages via postoffice'

    def handle(self, *args, **kwargs):
        configure_publishers()
