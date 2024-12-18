from django.urls import path
from backend.views import *

urlpatterns = [
    path('profile/<int:user_id>/', profile_page),
    path('notifications/', notifications, name='notifications'),
    path('applications/<int:application_id>', single_application_page),
    path('reply_to_request/', reply_to_request),
    path('complete_application/', complete_application),
    path('edit_profile/', ProfileEdit.as_view()),
    path('tutor_cards/', Tutors.as_view()),
    path('applications/', applications_page, name='applications'),
    path('add_application/', add_application),
    # path('add_comment/', add_comment),
    # path('like_question/', like_question),
    # path('like_comment/', like_comment),
    path('application_form/', application_form),
    path('mentor_application/', mentor_application)
]
