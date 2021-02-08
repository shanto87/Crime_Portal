from django.contrib import admin
from .models import Authentication, Registered_Users, WantedCriminals, AreaName, GeneralDiary, GeneralDiaryByUsers, PSNames, CrimeNews, LocalIntelligence

# Register your models here.

admin.site.register(Authentication)
admin.site.register(Registered_Users)
admin.site.register(WantedCriminals)
admin.site.register(AreaName)
admin.site.register(GeneralDiaryByUsers)
admin.site.register(GeneralDiary)
admin.site.register(PSNames)
admin.site.register(CrimeNews)
admin.site.register(LocalIntelligence)

