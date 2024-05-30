import datetime

from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *


def index(request):
    user = request.user
    questions = Question.objects.filter(status='Не решён')
    tutors = UserProfile.objects.filter(status='Наставник')

    return render(request, 'index.html', {'user': user, 'questions': questions, 'tutors': tutors})


def tutors_page(request):
    user = request.user
    tutors = UserProfile.objects.filter(status='Наставник')
    return render(request, 'tutor_cards.html', {'user': user, 'tutors': tutors})


def profile_page(request, user_id):
    user = request.user

    profile = UserProfile.objects.get(user=User.objects.get(id=user_id))
    specialization_list = []

    if len(profile.specialization_1) > 1:
        specialization_list.append(profile.specialization_1)
    if len(profile.specialization_2) > 1:
        specialization_list.append(profile.specialization_2)
    if len(profile.specialization_3) > 1:
        specialization_list.append(profile.specialization_3)
    if len(profile.specialization_4) > 1:
        specialization_list.append(profile.specialization_4)
    if len(profile.specialization_5) > 1:
        specialization_list.append(profile.specialization_5)

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'specialization_list': specialization_list
    })


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

        if request.FILES:
            file = request.FILES[f'profile{profile.id}_photo']
            profile.photo = file

        profile.save()
        return redirect(f'/profile/{profile.user.id}/')


def questions_page(request):
    user = request.user

    questions = Question.objects.all().order_by('-likes', '-datetime')
    comments = Commentary.objects.all().order_by('-likes', '-datetime')
    user_likes = Like.objects.filter(user=request.user)
    liked_questions = {like.question: 1 for like in user_likes if like.question is not None}
    liked_comments = {like.comment: 1 for like in user_likes}

    return render(request, 'questions.html', {'user': user,
                                              'questions': questions,
                                              'comments': comments,
                                              'liked_questions': liked_questions,
                                              'liked_comments': liked_comments})


@api_view(['POST'])
def add_question(request):
    author = UserProfile.objects.get(user=request.user)
    text = request.POST.get('question')
    Question.objects.create(author=author, text=text, datetime=datetime.datetime.now())

    return redirect('questions')


@api_view(['POST'])
def add_comment(request):
    author = UserProfile.objects.get(user=request.user)
    question = Question.objects.get(id=request.POST.get('question_id'))
    text = request.POST.get('comment')
    Commentary.objects.create(author=author, text=text, question=question, datetime=datetime.datetime.now())

    if question.comments_count == 0:
        question.status = 'Не решён'

    question.addComment()

    return redirect('questions')


@api_view(['POST'])
def like_question(request):
    question_id = request.POST.get('question_id')
    question = Question.objects.get(id=question_id)

    question.addLike()

    # like = Like.objects.filter(user=request.user, question=question)
    # if len(like) != 0:
    #     like.delete()
    # else:
    #     Like.objects.create(user=request.user, question=question)
    #     question.addLike()

    return redirect('questions')


@api_view(['POST'])
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Commentary.objects.get(id=comment_id)
    comment.addLike()

    # like = Like.objects.filter(user=request.user, comment=comment)
    # if len(like) != 0:
    #     like.delete()
    # else:
    #     Like.objects.create(user=request.user, comment=comment)
    #     comment.addLike()

    return redirect('questions')
