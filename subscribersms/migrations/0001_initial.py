# Generated by Django 4.0.4 on 2022-05-21 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriberSMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create date')),
                ('phone', models.CharField(max_length=30, unique=True, verbose_name='phone')),
                ('gdpr_consent', models.BooleanField(default=False, verbose_name='gdpr consent')),
            ],
            options={
                'verbose_name': 'SubscriberSMS',
                'verbose_name_plural': 'SubscriberSMS',
            },
        ),
    ]
