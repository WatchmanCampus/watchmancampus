from django.db import models

# Create your models here.

QUESTION_TYPE = (
    ('Multiple Choice', 'Multiple Choice'),
    ('Checkboxes', 'Checkboxes'),
    ('Dropdown', 'Dropdown'),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)


class GoogleFormData(BaseModel):
    title = models.CharField(max_length=200, default="Untitled document")
    description = models.TextField(blank=True, null=True)


class Question(BaseModel):
    # google_form = models.ForeignKey(GoogleFormData, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default="Question")
    description = models.TextField(blank=True, null=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE, default="Multiple Choice")
    # image = Image
    # video = video
    is_required = models.BooleanField(default=False)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False)
    question_choices = models.CharField(max_length=250, null=False, blank=False)
    file = models.ImageField(upload_to='choice_image')


class Answer(models.Model):
    answer = models.CharField(max_length=250, null=False, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False)


class Response(BaseModel):
    resp_id = models.CharField(null=False, blank=False, max_length=10)
    form = models.ForeignKey(GoogleFormData, on_delete=models.CASCADE, null=False, blank=False)
    answer = models.ManyToManyField(Answer)
