from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
    ordering = ('id',)


admin.site.register(User, UserAdmin)
