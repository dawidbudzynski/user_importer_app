from django.core.management.base import BaseCommand

from user.constants import ALLOWED_IMPORT_TYPES
from user.importers import SubscriberImporter


class Command(BaseCommand):
    help = 'Create Users based on Subscribers or SubscribersSMS'

    def add_arguments(self, parser):
        parser.add_argument('--import_type', type=str)

    def handle(self, *args, **options):
        import_type = options['import_type']
        if import_type not in ALLOWED_IMPORT_TYPES:
            print(f'Wrong import type. Allowed types {ALLOWED_IMPORT_TYPES}')
        importer = SubscriberImporter()
        importer.start_import(import_type=import_type)
