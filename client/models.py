from django.db import models


class Client(models.Model):
    create_date = models.DateTimeField(verbose_name='create date', auto_now_add=True)
    email = models.EmailField(verbose_name='email', unique=True)
    phone = models.CharField(verbose_name='phone', max_length=30)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.id} - {self.email}'
