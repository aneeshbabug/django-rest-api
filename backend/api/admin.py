from django.contrib import admin
from .models import BackendUser, Item

# Register your models here.
admin.site.register(Item)
admin.site.register(BackendUser)
