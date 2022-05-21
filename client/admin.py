from django.contrib import admin

from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    ordering = ('id', )
    list_display = ("__str__", 'create_date')


admin.site.register(Client, ClientAdmin)
