from django.core.management.base import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = 'Create Users based on Subscribers'

    def handle(self, *args, **options):
        User.import_subscribers()
