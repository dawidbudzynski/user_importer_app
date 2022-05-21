from django.contrib import admin

from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    ordering = ('id', )


admin.site.register(Client, ClientAdmin)
