from django.db import models


class User(models.Model):
    create_date = models.DateTimeField(verbose_name='create date', auto_created=True)
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(verbose_name='phone', max_length=30)
    gdpr_consent = models.BooleanField(verbose_name='gdpr consent')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id} - {self.email}'
