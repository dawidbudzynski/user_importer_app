from django.db import connection  # todo remove later
from django.db import models
from django.db.models import Q

from client.models import Client
from subscriber.models import Subscriber
from user.constants import ConflictReason


class User(models.Model):
    create_date = models.DateTimeField(verbose_name='create date', auto_now_add=True)
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(verbose_name='phone', max_length=30)
    gdpr_consent = models.BooleanField(verbose_name='gdpr consent')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id} - {self.email}'

    @classmethod
    def import_subscribers(cls):
        all_user_emails = User.objects.all().values_list('email', flat=True)
        all_user_phones = User.objects.all().values_list('phone', flat=True)
        all_client_emails = Client.objects.all().values_list('email', flat=True)
        all_client_phones = Client.objects.all().values_list('phone', flat=True)

        users_to_create = []
        conflicts = []

        for subscriber in Subscriber.objects.all():
            if subscriber.email in all_user_emails:
                continue

            if subscriber.email in all_client_emails:
                matching_client = Client.objects.get(email=subscriber.email)

                if list(all_client_phones).count(matching_client.phone) > 1:
                    conflicts.append({
                        'id': subscriber.id, 'email': subscriber.email,
                        'reason': ConflictReason.CLIENT_PHONE_NOT_UNIQUE
                    })
                    continue

                if matching_client.phone in all_user_phones:
                    matching_users = User.objects.filter(
                        Q(phone=matching_client.phone) & ~Q(email=matching_client.email)
                    )
                    if matching_users:
                        conflicts.append({
                            'id': subscriber.id, 'email': subscriber.email,
                            'reason': ConflictReason.USER_CONFLICT
                        })
                        continue
                # create user using client data
                new_user = User(
                    email=matching_client.email,
                    phone=matching_client.phone,
                    gdpr_consent=subscriber.gdpr_consent
                )
                users_to_create.append(new_user)
            else:
                # create user using subscriber data
                new_user = User(
                    email=subscriber.email,
                    gdpr_consent=subscriber.gdpr_consent
                )
                users_to_create.append(new_user)

        User.objects.bulk_create(users_to_create)

        import pdb;pdb.set_trace()

        if conflicts:
            # todo add later
            # create_conflict_report(conflicts)
            print('generating conflict report')

        print(f'Database hits: {len(connection.queries)}')  # todo remove later
