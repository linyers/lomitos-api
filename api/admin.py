from django.contrib import admin

from .models import Lomito, DayTime, NightTime, Rating

admin.site.register(Lomito)
admin.site.register(DayTime)
admin.site.register(NightTime)
admin.site.register(Rating)