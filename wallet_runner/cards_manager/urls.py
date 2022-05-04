from django.urls import path
from . import views

urlpatterns = [
    path('SortMyCards/', views.SortMyCardsView.as_view(), name='SortMyCards'),
]