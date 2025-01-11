from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Application)
admin.site.register(MentorApplication)
# admin.site.register(Commentary)

