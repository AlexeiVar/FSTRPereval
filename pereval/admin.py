from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(CustomUser, UserAdmin)

admin.site.register(Level)
admin.site.register(Coords)
admin.site.register(Images)
admin.site.register(PerevalAdded)
