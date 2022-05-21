from django.contrib import admin

from subscribersms.models import SubscriberSMS


class SubscriberSMSAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ("__str__", 'create_date')


admin.site.register(SubscriberSMS, SubscriberSMSAdmin)
