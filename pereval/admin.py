from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+ (
        (
            'Personal info',
            {
                'fields': (
                    'phone',
                    'name',
                    'fam',
                    'otc',
                ),
            },
        ),
    )




admin.site.register(Level)
admin.site.register(Coords)
admin.site.register(Images)


@admin.register(Pereval)
class PerevalAdmin(admin.ModelAdmin):
    readonly_fields = ('add_time',)