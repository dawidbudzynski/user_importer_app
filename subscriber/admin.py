from django.contrib import admin

from subscriber.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    ordering = ('id',)


admin.site.register(Subscriber, SubscriberAdmin)
