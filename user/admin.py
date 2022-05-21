from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ("__str__", 'create_date')


admin.site.register(User, UserAdmin)
