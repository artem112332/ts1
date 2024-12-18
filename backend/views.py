from datetime import datetime, date
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *


def index(request):
    user = request.user
    applications = Application.objects.filter(type='Общая', status='Активна')
    tutors = UserProfile.objects.filter(status='Наставник')

    return render(request, 'index.html', {'user': user, 'applications': applications, 'tutors': tutors})


def mentor_application(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    return render(request, 'mentor_application.html', {'profile': profile})


class Tutors(APIView):
    def get(self, request):
        user = request.user
        tutors = UserProfile.objects.filter(status='Наставник')
        tutors_specializations = {tutor: ', '.join(tutor.get_specializations()) for tutor in tutors}
        filters = 5 * ['']

        return render(request, 'tutor_cards.html', {
            'user': user,
            'tutors': tutors,
            'tutors_specializations': tutors_specializations,
            'filters': filters
        })

    def post(self, request):
        user = request.user

        filters = 5 * ['']
        if request.POST.get('Аналитика') is not None: filters[0] = 'Аналитика'
        if request.POST.get('Дизайн') is not None: filters[1] = 'Дизайн'
        if request.POST.get('Frontend') is not None: filters[2] = 'Frontend'
        if request.POST.get('Backend') is not None: filters[3] = 'Backend'
        if request.POST.get('Teamlead') is not None: filters[4] = 'Teamlead'

        tutors = UserProfile.objects.filter(status='Наставник')

        if filters[0] != '':
            tutors = tutors.filter(specialization_1=filters[0])
        if filters[1] != '':
            tutors = tutors.filter(specialization_2=filters[1])
        if filters[2] != '':
            tutors = tutors.filter(specialization_3=filters[2])
        if filters[3] != '':
            tutors = tutors.filter(specialization_4=filters[3])
        if filters[4] != '':
            tutors = tutors.filter(specialization_5=filters[4])

        tutors_specializations = {tutor: ', '.join(tutor.get_specializations()) for tutor in tutors}

        return render(request, 'tutor_cards.html', {
            'user': user,
            'tutors': tutors,
            'tutors_specializations': tutors_specializations,
            'filters': filters
        })


def profile_page(request, user_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    profile = UserProfile.objects.get(user=User.objects.get(id=user_id))
    telegram = False
    if user_profile == profile:
        telegram = True

    if profile.status == 'Наставник':
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

        accepted_applications = Application.objects.filter(reciever=profile, sender=user_profile, status='Принята')
        if len(accepted_applications) > 0:
            telegram = True

        return render(request, 'profile.html', {
            'user': user,
            'profile': profile,
            'specialization_list': specialization_list,
            'user_profile': user_profile,
            'telegram': telegram,
        })

    elif user_profile.status == 'Наставник':
        accepted_applications = Application.objects.filter(reciever=user_profile, sender=profile, status='Принята')

        if len(accepted_applications) > 0:
            telegram = True

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'telegram': telegram,
    })


class ProfileEdit(APIView):
    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if profile.status == 'Наставник':
            is_mentor = True
        else:
            is_mentor = False

        return render(request, 'lk_edit.html', {
            'profile': profile,
            'is_mentor': is_mentor
        })

    def post(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if request.FILES:
            file = request.FILES[f'profile{profile.id}_photo']
            profile.photo = file

        profile.last_name = request.POST.get('last_name')
        profile.first_name = request.POST.get('first_name')
        profile.middle_name = request.POST.get('middle_name')
        profile.telegram = request.POST.get('telegram')

        if request.POST.get('description') is not None:
            profile.description = request.POST.get('description')

        if profile.status == 'Наставник':
            if request.POST.get('Аналитика') is not None:
                profile.specialization_1 = 'Аналитика'
            if request.POST.get('Дизайн') is not None:
                profile.specialization_2 = 'Дизайн'
            if request.POST.get('Frontend') is not None:
                profile.specialization_3 = 'Frontend'
            if request.POST.get('Backend') is not None:
                profile.specialization_4 = 'Backend'
            if request.POST.get('Teamlead') is not None:
                profile.specialization_5 = 'Teamlead'

        profile.save()
        return redirect(f'/profile/{user.id}/')


def notifications(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if profile.status == 'Наставник':
        applications = Application.objects.filter(reciever=profile)
        return render(request, 'notifications_projectant.html', {
            'user': user,
            'applications': applications
        })

    # elif profile.is_admin:


    applications = Application.objects.filter(sender=profile).order_by('status')
    return render(request, 'notifications_mentor.html', {
        'user': user,
        'applications': applications
    })


def single_application_page(request, application_id):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    application = Application.objects.get(id=application_id)

    return render(request, 'application.html', {'application': application, 'profile': profile})


@api_view(['POST'])
def complete_application(request):
    application = Application.objects.get(id=request.POST.get('application_id'))
    application.complete()

    return redirect('notifications')


@api_view(['POST'])
def reply_to_request(request):
    application_id = request.POST.get('application_id')
    mentor_id = request.POST.get('mentor_id')

    mentor = UserProfile.objects.get(id=mentor_id)
    application = Application.objects.get(id=application_id)
    application.reciever = mentor

    reply = request.POST.get('reply')
    if reply == 'Принять':
        application.accept()
    else:
        application.decline()

    return redirect('notifications')


def applications_page(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    applications = Application.objects.filter(type='Общая', status='Активна').order_by('-datetime')
    # comments = Commentary.objects.all().order_by('-likes', '-datetime')
    # user_likes = Like.objects.filter(user=request.user)
    # liked_consult_requests = [like.consult_request for like in user_likes if like.consult_request is not None]
    # liked_comments = [like.comment for like in user_likes]

    return render(request, 'questions.html', {'user': user,
                                              'user_profile': user_profile,
                                              'applications': applications,
                                              # 'comments': comments,
                                              # 'liked_Applications': liked_Applications,
                                              # 'liked_comments': liked_comments
                                              })


@api_view(['GET'])
def application_form(request):
    appl_type = 'Общая'

    if request.GET.get('mentor') is not None:
        mentor_id = request.GET.get('mentor')
        mentor = UserProfile.objects.get(id=mentor_id)
        appl_type = 'Личная'

        return render(request, 'application_form.html',
                      {'mentor': mentor, 'appl_type': appl_type, 'mentor_id': mentor_id})

    return render(request, 'application_form.html', {'appl_type': appl_type})


@api_view(['POST'])
def add_application(request):
    sender = UserProfile.objects.get(user=request.user)
    title = request.POST.get('title')
    description = request.POST.get('description')
    application = Application.objects.create(sender=sender, title=title, description=description,
                                             datetime=datetime.now())

    if request.POST.get('appl_type') == 'Личная':
        reciever_id = request.POST.get('reciever_id')
        application.reciever = UserProfile.objects.get(id=reciever_id)
        application.type = 'Личная'
        application.save()

    # TODO вложения
    return redirect('applications')

# @api_view(['POST'])
# def add_comment(request):
#     author = UserProfile.objects.get(user=request.user)
#     consult_request = Application.objects.get(id=request.POST.get('Application_id'))
#     text = request.POST.get('comment')
#     Commentary.objects.create(author=author, text=text, Application=Application,
#                               datetime=datetime.now())
#
#     if Application.comments_count == 0:
#         Application.status = 'Не решён'
#
#     consult_request.addComment()
#
#     return redirect('Applications')


# @api_view(['POST'])
# def like_Application(request):
#     consult_request_id = request.POST.get('Application_id')
#     consult_request = Application.objects.get(id=consult_request_id)
#
#     like = Like.objects.filter(user=request.user, Application=Application)
#     if len(like) != 0:
#         consult_request.deleteLike()
#         like.delete()
#     else:
#         Like.objects.create(user=request.user, Application=Application)
#         consult_request.addLike()
#
#     return redirect('Applications')
#
#
# @api_view(['POST'])
# def like_comment(request):
#     comment_id = request.POST.get('comment_id')
#     comment = Commentary.objects.get(id=comment_id)
#
#     like = Like.objects.filter(user=request.user, comment=comment)
#     if len(like) != 0:
#         comment.deleteLike()
#         like.delete()
#     else:
#         Like.objects.create(user=request.user, comment=comment)
#         comment.addLike()
#
#     return redirect('Applications')
