from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import QuestionForm, CommentaryForm
from .models import *


def index(request):
    return render(request, 'index.html')


def profile_page(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'lk.html', {'profile': profile})


class ProfileEdit(APIView):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'lk_edit.html', {'profile': profile})

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)

        profile.last_name = request.POST.get('last_name')
        profile.first_name = request.POST.get('first_name')
        profile.middle_name = request.POST.get('middle_name')
        profile.email = request.POST.get('email')

        if request.POST.get('description') is not None:
            profile.description = request.POST.get('description')

        if request.POST.get('Аналитика') is not None:
            profile.specialization_1 = request.POST.get('Аналитика')
        if request.POST.get('Дизайн') is not None:
            profile.specialization_2 = request.POST.get('Дизайн')
        if request.POST.get('Frontend') is not None:
            profile.specialization_3 = request.POST.get('Frontend')
        if request.POST.get('Backend') is not None:
            profile.specialization_4 = request.POST.get('Backend')
        if request.POST.get('Teamlead') is not None:
            profile.specialization_5 = request.POST.get('Teamlead')

        profile.save()
        return render(request, 'lk.html', {'profile': profile})


class AddQuestion(APIView):
    def get(self, request):
        form = QuestionForm
        return render(request, 'add_question.html', {'form': form})

    def post(self, request):
        form = QuestionForm(request.POST)
        return render(request, 'add_question.html', {'form': form})


def questions_page(request):
    questions = Question.objects.all()
    return render(request, 'questions.html', {'questions': questions})
