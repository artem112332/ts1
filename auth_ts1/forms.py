from django import forms
from django.contrib.auth.models import User
from backend.models import UserProfile


class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, '', password)
        if commit:
            user.save()
        return user


class UserProfileForm(forms.Form):
    last_name = forms.CharField
    first_name = forms.CharField
    middle_name = forms.CharField
    status = forms.CharField

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'middle_name', 'status']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, '', password)
        if commit:
            user.save()
        return user
