from django.urls import path
from .views import home, create_form, add_question, edit_question


urlpatterns = [
    path('', home, name='form-home'),
    path('create/', create_form, name='form-create')
]

htmx_urlpatterns = [
    path('add-question/', add_question, name='add-question'),
    path('edit-question/<int:pk>/edit', edit_question, name='edit-question'),

]

urlpatterns += htmx_urlpatterns
