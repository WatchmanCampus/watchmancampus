from django.contrib import admin

# Register your models here.
from .models import GoogleFormData, Question, Choice, Answer, Response

admin.site.register(GoogleFormData)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Response)
