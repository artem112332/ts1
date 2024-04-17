from django import forms
from .models import Question, Commentary


class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'Placeholder': 'Коротко опишите ваш вопрос'}),
                            label='Вопрос')
    text = forms.CharField(widget=forms.Textarea(attrs={'Placeholder': 'Опишите вопрос подробнее'}),
                           label='Подробности')

    class Meta:
        model = Question
        fields = ['title', 'text']

    def save(self, commit=True):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        author = self.cleaned_data['author']
        question = Question.objects.create(title=title, text=text)
        if commit:
            question.save()
        return question


class CommentaryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'Placeholder': 'Text'}))

    class Meta:
        model = Commentary
        fields = ['text']

    def save(self, commit=True):
        text = self.cleaned_data['text']
        commentary = Commentary.objects.create(text=text)
        if commit:
            commentary.save()
        return commentary
