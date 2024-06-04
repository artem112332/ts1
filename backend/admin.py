from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Commentary)
admin.site.register(Consultation)
admin.site.register(Week)
admin.site.register(Day)