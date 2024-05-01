from django.urls import path
from backend.views import *

urlpatterns = [
    path('add_question/', AddQuestion.as_view(), name='add_question'),
    path('edit_profile/', ProfileEdit.as_view(), name='edit_profile')
]
