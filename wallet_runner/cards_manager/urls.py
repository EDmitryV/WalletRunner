from django.urls import path
from . import views

urlpatterns = [
    path('SortMyCards', views.sort_my_cards, name='SortMyCards'),
]