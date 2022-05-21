from django.contrib import admin

from subscribersms.models import SubscriberSMS


class SubscriberSMSAdmin(admin.ModelAdmin):
    ordering = ('id',)


admin.site.register(SubscriberSMS, SubscriberSMSAdmin)
