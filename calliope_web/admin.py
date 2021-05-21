from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Bss


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Bss)

