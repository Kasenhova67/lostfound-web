from django.contrib import admin
from .models import Profile, itemlostfull, itemfoundfull

admin.site.register(Profile)
admin.site.register(itemlostfull)
admin.site.register(itemfoundfull)
