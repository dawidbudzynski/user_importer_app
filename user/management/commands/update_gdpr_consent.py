from itertools import islice

from django.core.management.base import BaseCommand

from subscriber.models import Subscriber
from subscribersms.models import SubscriberSMS
from user.models import User

BATCH_SIZE = 10000


class Command(BaseCommand):
    help = 'Update gdpr consent'

    def __init__(self):
        self.users_to_update = []

    def handle(self, *args, **options):
        self.update_users_with_matching_subscribers()
        self.update_users_created_from_subscribers()
        self.update_users_created_from_subscriberssms()

        if self.users_to_update:
            self.update_users_in_batches()

    def update_users_in_batches(self):
        objects_to_update = (user for user in self.users_to_update)
        while True:
            batch = list(islice(objects_to_update, BATCH_SIZE))
            if not batch:
                break
            User.objects.bulk_update(batch, fields=['create_date'], batch_size=BATCH_SIZE)

    def update_users_with_matching_subscribers(self):
        all_user_emails = User.objects.all().values_list('email', flat=True)
        subscribers_with_matching_users_data = {
            subscriber.email: subscriber.create_date
            for subscriber in Subscriber.objects.all()
            if subscriber.email in all_user_emails
        }

        matching_users = User.objects.filter(email__in=subscribers_with_matching_users_data.keys())

        for user in matching_users:
            subscriber_create_date = subscribers_with_matching_users_data.get(user.email)
            if subscriber_create_date > user.create_date:
                user.create_date = subscriber_create_date
                self.users_to_update.append(user)

    def update_users_created_from_subscribers(self):
        users_imported_from_subscribers = User.objects.filter(imported_from_subscriber=True)
        matching_subscribers = Subscriber.objects.filter(
            email__in=users_imported_from_subscribers.values_list('email', flat=True)
        )
        subscribers_with_matching_users_data = {
            subscriber.email: subscriber.create_date
            for subscriber in matching_subscribers
        }
        for user in users_imported_from_subscribers:
            subscriber_create_date = subscribers_with_matching_users_data.get(user.email)
            if subscriber_create_date > user.create_date:
                user.create_date = subscriber_create_date
                self.users_to_update.append(user)

    def update_users_created_from_subscriberssms(self):
        users_imported_from_subscriberssms = User.objects.filter(imported_from_subscribersms=True)
        matching_subscribers = SubscriberSMS.objects.filter(
            phone__in=users_imported_from_subscriberssms.values_list('phone', flat=True)
        )
        subscribers_with_matching_users_data = {
            subscriber.phone: subscriber.create_date
            for subscriber in matching_subscribers
        }
        for user in users_imported_from_subscriberssms:
            subscriber_create_date = subscribers_with_matching_users_data.get(user.phone)
            if subscriber_create_date > user.create_date:
                user.create_date = subscriber_create_date
                self.users_to_update.append(user)
