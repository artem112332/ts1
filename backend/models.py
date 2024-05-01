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
    photo = models.ImageField(upload_to='users_photo/', blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def full_name(self):
        return self.__str__

    def last_and_first_name(self):
        return f'{self.first_name} {self.last_name}'

    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'


class Question(models.Model):
    author = models.ForeignKey(UserProfile, models.CASCADE)
    status_choices = [
        ('NK', 'Нет комментариев'),
        ('NA', 'Не решён'),
        ('AF', 'Решён')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Нет комментариев')
    # title = models.TextField(max_length=150)
    text = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    datetime = models.DateTimeField
    specialization_1 = models.CharField(max_length=20, choices=specialization_choices)
    specialization_2 = models.CharField(max_length=20, choices=specialization_choices)
    specialization_3 = models.CharField(max_length=20, choices=specialization_choices)

    def addLike(self):
        self.likes += 1

    def __str__(self):
        return f'№{self.id}{self.author.short_name}: {self.text[:20]}'


class Commentary(models.Model):
    author = models.ForeignKey(UserProfile, models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    has_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    datetime = models.DateTimeField
    likes = models.IntegerField(default=0)
    is_answer = models.BooleanField(default=False)
    text = models.TextField(max_length=500)

    def addLike(self):
        self.likes += 1

    def mark_as_answer(self):
        self.is_answer = True

    def __str__(self):
        return f'Вопрос №{self.question.id} Автор: {self.author.short_name}'


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
    join_link = models.CharField(max_length=150)

    def set_accepted(self):
        self.status = 'Принят'

    def set_declined(self):
        self.status = 'Отклонён'

    def __str__(self):
        return f'Id {self.id} Кому: {self.mentor.short_name} От: {self.author_of_request.short_name}'
