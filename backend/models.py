from django.db import models
from django.contrib.auth.models import User

specialization_choices = [
    ('Teamlead', 'Teamlead'),
    ('Backend', 'Backend'),
    ('Frontend', 'Frontend'),
    ('Дизайн', 'Дизайн'),
    ('Аналитика', 'Аналитика'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    last_name = models.CharField(max_length=50)  # Фамилия
    first_name = models.CharField(max_length=50)  # Имя
    middle_name = models.CharField(max_length=50)  # Отчество
    status_choises = [
        ('Проектант', 'Проектант'),
        ('Наставник', 'Наставник')
    ]
    status = models.CharField(max_length=20, choices=status_choises, default='Проектант')
    have_schedule = models.BooleanField(default=False)
    specialization_1 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_2 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_3 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_4 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_5 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to='users_photo/', blank=True, default='default_avatar.jpeg')

    def get_specializations(self):
        specializations = []
        if self.specialization_1 != '': specializations.append(self.specialization_1)
        if self.specialization_2 != '': specializations.append(self.specialization_2)
        if self.specialization_3 != '': specializations.append(self.specialization_3)
        if self.specialization_4 != '': specializations.append(self.specialization_4)
        if self.specialization_5 != '': specializations.append(self.specialization_5)

        return specializations

    def addSchedule(self):
        self.have_schedule = True
        self.save()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def full_name(self):
        return self.__str__

    def first_and_last_name(self):
        return f'{self.first_name} {self.last_name}'

    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'


class Question(models.Model):
    author = models.ForeignKey(UserProfile, models.CASCADE)
    status_choices = [
        ('Нет комментариев', 'Нет комментариев'),
        ('Не решён', 'Не решён'),
        ('Решён', 'Решён')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Нет комментариев')
    text = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    datetime = models.DateTimeField(blank=True)
    is_new = models.BooleanField(default=True)
    comments_count = models.IntegerField(default=0)

    def answer_found(self):
        self.status = 'Решён'
        self.save()

    def addComment(self):
        self.comments_count += 1
        self.save()

    def addLike(self):
        self.likes += 1
        self.save()

    def deleteLike(self):
        if self.likes >= 1:
            self.likes -= 1
        self.save()

    def __str__(self):
        return f'№{self.id} {self.author.short_name()}: {self.text[:20]}'


class Commentary(models.Model):
    author = models.ForeignKey(UserProfile, models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    likes = models.IntegerField(default=0)
    is_answer = models.BooleanField(default=False)
    text = models.TextField(max_length=500)

    def addLike(self):
        self.likes += 1
        self.save()

    def deleteLike(self):
        if self.likes >= 1:
            self.likes -= 1
        self.save()

    def mark_as_answer(self):
        self.is_answer = True
        self.save()

    def __str__(self):
        return f'id:{self.id} "{self.text}" под вопросом №{self.question.id} от {self.author.short_name()}'


class Like(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='+')
    question = models.ForeignKey(Question, models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Commentary, models.CASCADE, related_name='+', blank=True, null=True)


class Consultation(models.Model):
    author_of_request = models.ForeignKey(UserProfile, models.CASCADE, related_name='+')
    mentor = models.ForeignKey(UserProfile, models.CASCADE, related_name='+')
    date = models.DateField()
    time = models.CharField(max_length=10)
    status_choices = [
        ('Отправлен', 'Отправлен'),
        ('Принят', 'Принят'),
        ('Отклонён', 'Отклонён')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Отправлен')
    commentary = models.TextField(max_length=500, blank=True)
    join_link = models.CharField(max_length=150)

    def set_accepted(self):
        self.status = 'Принят'
        self.save()

    def set_declined(self):
        self.status = 'Отклонён'
        self.save()

    def __str__(self):
        return f'Id {self.id} Кому: {self.mentor.short_name()} От: {self.author_of_request.short_name()}'


class Day(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    time_choices = [
        ('Свободно', 'Свободно'),
        ('Недоступно', 'Недоступно'),
        ('Занято', 'Занято')
    ]
    date = models.DateField(blank=True, null=True)
    time_9to10 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_10to11 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_11to12 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_12to13 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_13to14 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_14to15 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_15to16 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_16to17 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_17to18 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_18to19 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_19to20 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_20to21 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
    time_21to22 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')

    @classmethod
    def get_default_pk(cls):
        day = cls.objects.create()
        return day.pk

    def set_times(self, times):
        self.time_9to10 = times['9']
        self.time_10to11 = times['10']
        self.time_11to12 = times['11']
        self.time_12to13 = times['12']
        self.time_13to14 = times['13']
        self.time_14to15 = times['14']
        self.time_15to16 = times['15']
        self.time_16to17 = times['16']
        self.time_17to18 = times['17']
        self.time_18to19 = times['18']
        self.time_19to20 = times['19']
        self.time_20to21 = times['20']
        self.time_21to22 = times['21']
        self.save()

    def get_times(self):
        times = {
            '9': self.time_9to10,
            '10': self.time_10to11,
            '11': self.time_11to12,
            '12': self.time_12to13,
            '13': self.time_13to14,
            '14': self.time_14to15,
            '15': self.time_15to16,
            '16': self.time_16to17,
            '17': self.time_17to18,
            '18': self.time_18to19,
            '19': self.time_19to20,
            '20': self.time_20to21,
            '21': self.time_21to22
        }
        return times


def get_default_times():
    times = {str(i): 'Недоступно' for i in range(9, 22)}
    return times


class Week(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='+')
    is_schedule = models.BooleanField(default=False)
    monday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
    tuesday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
    wednesday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
    thursday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
    friday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
    saturday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
    sunday = models.OneToOneField(Day, models.CASCADE, related_name='+', null=True, default=Day.get_default_pk)
