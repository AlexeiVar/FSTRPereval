from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Level)
admin.site.register(Coords)
admin.site.register(Images)


@admin.register(Pereval)
class PerevalAdmin(admin.ModelAdmin):
    readonly_fields = ('add_time',)