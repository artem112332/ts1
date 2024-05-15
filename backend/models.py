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
    specialization_1 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_2 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_3 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_4 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    specialization_5 = models.CharField(max_length=20, choices=specialization_choices, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to='users_photo/', blank=True, default='default_avatar.jpeg')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def full_name(self):
        return self.__str__

    def last_and_first_name(self):
        return f'{self.last_name} {self.first_name}'

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

    def mark_as_answer(self):
        self.is_answer = True

    def __str__(self):
        return f'id:{self.id} "{self.text}" под вопросом №{self.question.id} от {self.author.short_name()}'


class Like(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='+')
    question = models.ForeignKey(Question, models.CASCADE, related_name='+', blank=True)
    comment = models.ForeignKey(Commentary, models.CASCADE, related_name='+', blank=True)



class Consultation(models.Model):
    author_of_request = models.ForeignKey(UserProfile, models.CASCADE, related_name='+')
    mentor = models.ForeignKey(UserProfile, models.CASCADE, related_name='+')
    date = models.DateField
    time = models.TimeField
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

    def set_declined(self):
        self.status = 'Отклонён'

    def __str__(self):
        return f'Id {self.id} Кому: {self.mentor.short_name()} От: {self.author_of_request.short_name()}'

# class Day(models.Model):
#     week = models.ForeignKey
#     week_day_choices = [
#         ('Понедельник', 'Понедельник'),
#         ('Вторник', 'Вторник'),
#         ('Среда', 'Среда'),
#         ('Четверг', 'Четверг'),
#         ('Пятница', 'Пятница'),
#         ('Суббота', 'Суббота'),
#         ('Воскресенье', 'Воскресенье')
#     ]
#     week_day = models.CharField(max_length=20, choices=week_day_choices)
#     time_choices = [
#         ('Свободно', 'Свободно'),
#         ('Недоступно', 'Недоступно'),
#         ('Занято', 'Занято')
#     ]
#     date = models.DateField
#     time_9 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_10 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_11 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_12 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_13 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_14 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_15 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_16 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_17 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_18 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_19 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_20 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
#     time_21 = models.CharField(max_length=15, choices=time_choices, default='Недоступно')
