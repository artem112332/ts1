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
    telegram = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
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

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def full_name(self):
        return self.__str__

    def first_and_last_name(self):
        return f'{self.first_name} {self.last_name}'

    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'

    def make_mentor(self):
        self.status = self.status_choises[3]
        self.save()


class Application(models.Model):
    sender = models.ForeignKey(UserProfile, models.CASCADE, related_name='application_sender', null=True)
    status_choices = [
        ('Активна', 'Активна'),
        ('Принята', 'Принята'),
        ('Отказано', 'Отказано')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Активна')
    type_choices = [
        ('Общая', 'Общая'),
        ('Личная', 'Личная')
    ]
    type = models.CharField(max_length=20, choices=type_choices, default='Общая')
    reciever = models.ForeignKey(UserProfile, models.CASCADE, related_name='application_reciever', null=True,
                                 blank=True)
    title = models.TextField(max_length=200)
    description = models.TextField(max_length=1000)
    datetime = models.DateTimeField(blank=True)
    mentor_comment = models.TextField(max_length=200, blank=True, null=True)

    # likes = models.IntegerField(default=0)
    # comments_count = models.IntegerField(default=0)

    def __str__(self):
        return f'№{self.id} {self.sender.short_name()}: {self.title[:20]}'

    def accept(self):
        self.status = 'Принята'
        self.save()

    def decline(self):
        self.status = 'Отказано'
        self.save()

    # def addComment(self):
    #     self.comments_count += 1
    #     self.save()
    #
    # def addLike(self):
    #     self.likes += 1
    #     self.save()
    #
    # def deleteLike(self):
    #     if self.likes >= 1:
    #         self.likes -= 1
    #     self.save()

# class Commentary(models.Model):
#     author = models.ForeignKey(UserProfile, models.CASCADE)
#     application = models.ForeignKey(Application, on_delete=models.CASCADE)
#     datetime = models.DateTimeField()
#     likes = models.IntegerField(default=0)
#     is_answer = models.BooleanField(default=False)
#     text = models.TextField(max_length=500)
#
#     def addLike(self):
#         self.likes += 1
#         self.save()
#
#     def deleteLike(self):
#         if self.likes >= 1:
#             self.likes -= 1
#         self.save()
#
#     def mark_as_answer(self):
#         self.is_answer = True
#         self.save()
#
#     def __str__(self):
#         return f'id:{self.id} "{self.text}" под вопросом №{self.application.id} от {self.author.short_name()}'


# class Like(models.Model):
#     user = models.ForeignKey(User, models.CASCADE, related_name='+')
#     application = models.ForeignKey(Application, models.CASCADE, related_name='+', blank=True, null=True)
#     comment = models.ForeignKey(Commentary, models.CASCADE, related_name='+', blank=True, null=True)
