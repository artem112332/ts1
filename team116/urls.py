from django.contrib import admin
from django.urls import path, include
from backend.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_ts1.urls')),
    path('add_question/', AddQuestion.as_view(), name='add_question'),

]
