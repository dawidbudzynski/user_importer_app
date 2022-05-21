from django.db import models


class SubscriberSMS(models.Model):
    create_date = models.DateTimeField(verbose_name='create date', auto_now_add=True)
    phone = models.CharField(verbose_name='phone', max_length=30, unique=True)
    gdpr_consent = models.BooleanField(verbose_name='gdpr consent', default=False)

    class Meta:
        verbose_name = 'SubscriberSMS'
        verbose_name_plural = 'SubscriberSMS'

    def __str__(self):
        return f'{self.id} - {self.phone}'
