from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *


def index(request):
    user = request.user
    questions = Question.objects.all()
    tutors = UserProfile.objects.filter(status='Наставник')

    return render(request, 'index.html', {'user': user, 'questions': questions, 'tutors': tutors})


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


def get_string_week_dates(base_date, start_day, end_day=None):
    monday = base_date - timedelta(days=base_date.isoweekday() - 1)
    week_dates = [str(monday + timedelta(days=i)).split(sep='-') for i in range(7)]
    return week_dates[start_day - 1:end_day or start_day]


def get_week_dates(base_date, start_day, end_day=None):
    monday = base_date - timedelta(days=base_date.isoweekday() - 1)
    week_dates = [monday + timedelta(days=i) for i in range(7)]
    return week_dates[start_day - 1:end_day or start_day]


def profile_page(request, user_id):
    user = request.user
    profile = UserProfile.objects.get(user=User.objects.get(id=user_id))

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

        string_week_dates = get_string_week_dates(datetime.now().date(), 1, 7)
        week_days = {
            'пн.': string_week_dates[0],  # ['год', 'месяц', 'день']
            'вт.': string_week_dates[1],
            'ср.': string_week_dates[2],
            'чт.': string_week_dates[3],
            'пт.': string_week_dates[4],
            'сб.': string_week_dates[5],
            'вс.': string_week_dates[6]
        }
        times = [x for x in range(9, 22)]

        week_dates = get_week_dates(datetime.now().date(), 1, 7)
        current_week, created = Week.objects.get_or_create(
            user=profile.user,
            is_schedule=False,
            monday=Day.objects.get_or_create(user=profile.user, date=week_dates[0])[0],
            tuesday=Day.objects.get_or_create(user=profile.user, date=week_dates[1])[0],
            wednesday=Day.objects.get_or_create(user=profile.user, date=week_dates[2])[0],
            thursday=Day.objects.get_or_create(user=profile.user, date=week_dates[3])[0],
            friday=Day.objects.get_or_create(user=profile.user, date=week_dates[4])[0],
            saturday=Day.objects.get_or_create(user=profile.user, date=week_dates[5])[0],
            sunday=Day.objects.get_or_create(user=profile.user, date=week_dates[6])[0],
        )

        week = {
            'пн.': current_week.monday.get_times(),
            'вт.': current_week.tuesday.get_times(),
            'ср.': current_week.wednesday.get_times(),
            'чт.': current_week.thursday.get_times(),
            'пт.': current_week.friday.get_times(),
            'сб.': current_week.saturday.get_times(),
            'вс.': current_week.sunday.get_times()
        }

        return render(request, 'profile.html', {
            'user': user,
            'profile': profile,
            'specialization_list': specialization_list,
            'week_days': week_days,
            'times': times,
            'week': week
        })

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile
    })


@api_view(['POST'])
def send_consult_request(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    mentor_id = request.POST.get('mentor')
    mentor_profile = UserProfile.objects.get(user_id=mentor_id)

    comment = request.POST.get('comment')
    date_time = request.POST.get('date_time').split()
    time = date_time[3]
    date_input = date(int(date_time[0]), int(date_time[1]), int(date_time[2]))

    Consultation.objects.create(author_of_request=profile, mentor=mentor_profile, date=date_input, time=time,
                                commentary=comment)

    return redirect(f'/profile/{mentor_id}/')


class ProfileEdit(APIView):
    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if profile.status == 'Наставник':
            is_mentor = True
        else:
            is_mentor = False

        if profile.status == 'Наставник':
            times = [x for x in range(9, 22)]
            week_dates = get_string_week_dates(datetime.now().date(), 1, 7)
            week_days = {
                'пн.': week_dates[0],  # ['год', 'месяц', 'день']
                'вт.': week_dates[1],
                'ср.': week_dates[2],
                'чт.': week_dates[3],
                'пт.': week_dates[4],
                'сб.': week_dates[5],
                'вс.': week_dates[6]
            }

            if profile.have_schedule:
                schedule = Week.objects.get(user=user, is_schedule=True)
            else:
                schedule = Week.objects.create(
                    user=profile.user,
                    is_schedule=True,
                    monday=Day.objects.create(user=profile.user),
                    tuesday=Day.objects.create(user=profile.user),
                    wednesday=Day.objects.create(user=profile.user),
                    thursday=Day.objects.create(user=profile.user),
                    friday=Day.objects.create(user=profile.user),
                    saturday=Day.objects.create(user=profile.user),
                    sunday=Day.objects.create(user=profile.user)
                )

            schedule_dict = {
                'Понедельник': schedule.monday.get_times(),
                'Вторник': schedule.tuesday.get_times(),
                'Среда': schedule.wednesday.get_times(),
                'Четверг': schedule.thursday.get_times(),
                'Пятница': schedule.friday.get_times(),
                'Суббота': schedule.saturday.get_times(),
                'Воскресенье': schedule.sunday.get_times(),
            }

            return render(request, 'lk_edit.html', {
                'profile': profile,
                'is_mentor': is_mentor,
                'times': times,
                'week_days': week_days,
                'schedule': schedule_dict
            })

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
        profile.email = request.POST.get('email')

        if request.POST.get('description') is not None:
            profile.description = request.POST.get('description')

        if profile.status == 'Наставник':
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

            if request.POST.get('want_consult') is not None:
                if not profile.have_schedule:
                    profile.have_schedule = True

                schedule = Week.objects.get(user=user, is_schedule=True)
                datetime_input = sorted(list(map(str.split, request.POST.getlist('date_times'))))

                if len(datetime_input) > 0:
                    set_schedule(user, schedule, datetime_input)

        profile.save()
        return redirect(f'/profile/{user.id}/')


def set_schedule(user, schedule, datetime_input):
    weekdays_timecells = {}

    for INPUT in datetime_input:
        if INPUT[0] not in weekdays_timecells:
            weekdays_timecells[INPUT[0]] = [INPUT[1]]
        else:
            weekdays_timecells[INPUT[0]].append(INPUT[1])

    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    times_dict = {}

    for weekday in weekdays:
        times_dict[weekday] = get_default_times()
        if weekday in weekdays_timecells:
            for time_cell in weekdays_timecells[weekday]:
                times_dict[weekday][time_cell] = 'Свободно'

    schedule.monday.set_times(times_dict['Понедельник'])
    schedule.tuesday.set_times(times_dict['Вторник'])
    schedule.wednesday.set_times(times_dict['Среда'])
    schedule.thursday.set_times(times_dict['Четверг'])
    schedule.friday.set_times(times_dict['Пятница'])
    schedule.saturday.set_times(times_dict['Суббота'])
    schedule.sunday.set_times(times_dict['Воскресенье'])

    week_dates = get_week_dates(datetime.now().date(), 1, 7)
    current_week, created = Week.objects.get_or_create(
        user=user,
        is_schedule=False,
        monday=Day.objects.get_or_create(user=user, date=week_dates[0])[0],
        tuesday=Day.objects.get_or_create(user=user, date=week_dates[1])[0],
        wednesday=Day.objects.get_or_create(user=user, date=week_dates[2])[0],
        thursday=Day.objects.get_or_create(user=user, date=week_dates[3])[0],
        friday=Day.objects.get_or_create(user=user, date=week_dates[4])[0],
        saturday=Day.objects.get_or_create(user=user, date=week_dates[5])[0],
        sunday=Day.objects.get_or_create(user=user, date=week_dates[6])[0],
    )

    current_week.monday.set_times(schedule.monday.get_times())
    current_week.tuesday.set_times(schedule.tuesday.get_times())
    current_week.wednesday.set_times(schedule.wednesday.get_times())
    current_week.thursday.set_times(schedule.thursday.get_times())
    current_week.friday.set_times(schedule.friday.get_times())
    current_week.saturday.set_times(schedule.saturday.get_times())
    current_week.sunday.set_times(schedule.sunday.get_times())


def notifications(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if profile.status == 'Наставник':
        requests = Consultation.objects.filter(mentor=profile, status='Отправлен')
        return render(request, 'notices.html', {
            'user': user,
            'requests': requests
        })

    requests = Consultation.objects.filter(author_of_request=profile)
    return render(request, 'notices_projector.html', {
        'user': user,
        'requests': requests
    })


def reply_to_request(request):
    consult_request_id = request.POST.get('request_id')
    consultation = Consultation.objects.get(id=consult_request_id)
    link = request.POST.get('link')
    reply = request.POST.get('reply')
    if reply == 'Принять':
        consultation.join_link = link
        consultation.set_accepted()
    else:
        consultation.set_declined()

    return redirect('notifications')


def questions_page(request):
    user = request.user

    questions = Question.objects.all().order_by('-likes', '-datetime')
    comments = Commentary.objects.all().order_by('-likes', '-datetime')
    user_likes = Like.objects.filter(user=request.user)
    liked_questions = [like.question for like in user_likes if like.question is not None]
    liked_comments = [like.comment for like in user_likes]

    return render(request, 'questions.html', {'user': user,
                                              'questions': questions,
                                              'comments': comments,
                                              'liked_questions': liked_questions,
                                              'liked_comments': liked_comments
                                              })


@api_view(['POST'])
def add_question(request):
    author = UserProfile.objects.get(user=request.user)
    text = request.POST.get('question')
    Question.objects.create(author=author, text=text, datetime=datetime.now())

    return redirect('questions')


@api_view(['POST'])
def add_comment(request):
    author = UserProfile.objects.get(user=request.user)
    question = Question.objects.get(id=request.POST.get('question_id'))
    text = request.POST.get('comment')
    Commentary.objects.create(author=author, text=text, question=question, datetime=datetime.now())

    if question.comments_count == 0:
        question.status = 'Не решён'

    question.addComment()

    return redirect('questions')


@api_view(['POST'])
def like_question(request):
    question_id = request.POST.get('question_id')
    question = Question.objects.get(id=question_id)

    like = Like.objects.filter(user=request.user, question=question)
    if len(like) != 0:
        question.deleteLike()
        like.delete()
    else:
        Like.objects.create(user=request.user, question=question)
        question.addLike()

    return redirect('questions')


@api_view(['POST'])
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Commentary.objects.get(id=comment_id)

    like = Like.objects.filter(user=request.user, comment=comment)
    if len(like) != 0:
        comment.deleteLike()
        like.delete()
    else:
        Like.objects.create(user=request.user, comment=comment)
        comment.addLike()

    return redirect('questions')
