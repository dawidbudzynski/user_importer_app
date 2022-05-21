from django.db import models


class Subscriber(models.Model):
    create_date = models.DateTimeField(verbose_name='create date', auto_now_add=True)
    email = models.EmailField(verbose_name='email', unique=True)
    gdpr_consent = models.BooleanField(verbose_name='gdpr consent')

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return f'{self.id} - {self.email}'
