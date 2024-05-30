from django.urls import path
from backend.views import *

urlpatterns = [
    path('profile/<int:user_id>/', profile_page, name='profile'),
    path('edit_profile/', ProfileEdit.as_view(), name='edit_profile'),
    path('tutor_cards/', tutors_page, name='tutors_page'),
    path('questions/', questions_page, name='questions'),
    path('add_question/', add_question, name='add_question'),
    path('add_comment/', add_comment, name='add_question'),
    path('like_question/', like_question, name='like_question'),
    path('like_comment/', like_comment, name='like_comment'),
]
