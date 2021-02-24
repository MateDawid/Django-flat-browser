from django.contrib import admin
from .models import Flat, WatchedList, RefreshToken

admin.site.register(Flat)
admin.site.register(WatchedList)
admin.site.register(RefreshToken)
