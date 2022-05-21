from django.contrib import admin

from subscriber.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ("__str__", 'create_date')


admin.site.register(Subscriber, SubscriberAdmin)
