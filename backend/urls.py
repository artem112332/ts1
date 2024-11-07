from django.urls import path
from backend.views import *

urlpatterns = [
    path('profile/<int:user_id>/', profile_page),
    path('send_consult_request/', send_consult_request),
    path('notifications/', notifications, name='notifications'),
    path('reply_to_request/', reply_to_request),
    path('edit_profile/', ProfileEdit.as_view()),
    path('tutor_cards/', Tutors.as_view()),
    path('questions/', questions_page, name='questions'),
    path('add_question/', add_question),
    path('add_comment/', add_comment),
    path('like_question/', like_question),
    path('like_comment/', like_comment),
]
