from django.contrib import admin
from .models import itemlost
from .models import itemfound
admin.site.register(itemlost)
admin.site.register(itemfound)