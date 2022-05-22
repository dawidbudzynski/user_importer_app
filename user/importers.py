from django.db.models import Q

from client.models import Client
from subscriber.models import Subscriber
from subscribersms.models import SubscriberSMS
from user.constants import ConflictReason, ALLOWED_IMPORT_TYPES
from user.models import User
from user.utils import create_conflict_report


class SubscriberImporter:
    def __init__(self):
        self.all_user_emails = User.objects.all().values_list('email', flat=True)
        self.all_user_phones = User.objects.all().values_list('phone', flat=True)
        self.all_client_emails = Client.objects.all().values_list('email', flat=True)
        self.all_client_phones = Client.objects.all().values_list('phone', flat=True)
        self.users_to_create = []
        self.conflicts = []

    def start_import(self, import_type):
        if import_type not in ALLOWED_IMPORT_TYPES:
            print(f'Wrong import type. Allowed types {ALLOWED_IMPORT_TYPES}')

        if import_type == 'Subscriber':
            self.import_subscribers()
        elif import_type == 'SubscriberSMS':
            self.import_subscriberssms()

        if self.users_to_create:
            User.objects.bulk_create(self.users_to_create)

        if self.conflicts:
            create_conflict_report(report_type=import_type, data=self.conflicts)

    def import_subscribers(self):
        for subscriber in Subscriber.objects.all():
            if subscriber.email in self.all_user_emails:
                continue

            if subscriber.email in self.all_client_emails:
                matching_client = Client.objects.get(email=subscriber.email)

                # check if client phone is not unique
                if list(self.all_client_phones).count(matching_client.phone) > 1:
                    self.conflicts.append({
                        'id': subscriber.id, 'email': subscriber.email,
                        'reason': ConflictReason.CLIENT_PHONE_NOT_UNIQUE.value
                    })
                    continue

                # check conflicts between client and user
                if matching_client.phone in self.all_user_phones:
                    matching_users = User.objects.filter(
                        Q(phone=matching_client.phone) & ~Q(email=matching_client.email)
                    )
                    if matching_users:
                        self.conflicts.append({
                            'id': subscriber.id, 'email': subscriber.email,
                            'reason': ConflictReason.USER_CONFLICT.value
                        })
                        continue

                # create user using client data
                new_user = User(
                    email=matching_client.email,
                    phone=matching_client.phone,
                    gdpr_consent=subscriber.gdpr_consent
                )
                self.users_to_create.append(new_user)
            else:
                # create user using subscriber data
                new_user = User(
                    email=subscriber.email,
                    gdpr_consent=subscriber.gdpr_consent,
                    imported_from_subscriber=True
                )
                self.users_to_create.append(new_user)

    def import_subscriberssms(self):
        for subscriber_sms in SubscriberSMS.objects.all():
            if subscriber_sms.phone in self.all_user_phones:
                continue

            if subscriber_sms.phone in self.all_client_phones:
                # get matching client and check if client phone is not unique
                try:
                    matching_client = Client.objects.get(phone=subscriber_sms.phone)
                except Client.MultipleObjectsReturned:
                    self.conflicts.append({
                        'id': subscriber_sms.id, 'phone': subscriber_sms.phone,
                        'reason': ConflictReason.CLIENT_PHONE_NOT_UNIQUE.value
                    })
                    continue

                # check conflicts between client and user
                if matching_client.email in self.all_user_emails:
                    matching_users = User.objects.filter(
                        Q(email=matching_client.email) & ~Q(phone=matching_client.phone)
                    )
                    if matching_users:
                        self.conflicts.append({
                            'id': subscriber_sms.id, 'phone': subscriber_sms.phone,
                            'reason': ConflictReason.USER_CONFLICT.value
                        })
                        continue

                # create user using client data
                new_user = User(
                    email=matching_client.email,
                    phone=matching_client.phone,
                    gdpr_consent=subscriber_sms.gdpr_consent
                )
                self.users_to_create.append(new_user)
            else:
                # create user using subscriber_sms data
                new_user = User(
                    phone=subscriber_sms.phone,
                    gdpr_consent=subscriber_sms.gdpr_consent,
                    imported_from_subscribersms=True
                )
                self.users_to_create.append(new_user)
