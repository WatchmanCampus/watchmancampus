from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateForm, QuestionForm
from .models import GoogleFormData, Question, Choice, Answer, Response
from django.http import QueryDict


# Create your views here.


def home(request):
    return render(request, 'googleform/home.html')


def create_form(request):

    form = CreateForm
    questions = Question.objects.all()

    context = {
        'form': form,
        'questions': questions
    }
    return render(request, 'googleform/form_create.html', context)


def add_question(request):
    question = Question.objects.create()
    return redirect('edit-question', pk=question.id)


def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm(instance=question)
    context = {"question": question, "form": form}
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = QuestionForm(data, instance=question)
        if form.is_valid():
            form.save()
            context = {"question": question, "form": form}
            return render(request, 'googleform/partials/question_details.html', context)
        context = {"question": question, "form": form}
        return render(request, 'googleform/partials/question_edit.html', context)
    context = {"question": question, "form": form}
    return render(request, 'googleform/partials/question_edit.html', context)
