from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', user_logout),
    path('registration/', Register.as_view(), name='registration'),
    path('users/<int:pk>/', UserDetail.as_view()),
]
