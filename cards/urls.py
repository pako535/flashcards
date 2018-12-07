from django.urls import path

from .views import main, add_word, learn, reset

urlpatterns = [
    path('', main, name='main'),
    path('add', add_word, name='add'),
    path('learn', learn, name='learn'),
    path('reset', reset)
]
