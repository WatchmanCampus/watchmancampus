from django import forms
from .models import GoogleFormData, Question, Choice, Answer, Response


class CreateForm(forms.ModelForm):

    class Meta:
        model = GoogleFormData
        exclude = ['created_at', 'updated_at']


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ['created_at', 'updated_at']
