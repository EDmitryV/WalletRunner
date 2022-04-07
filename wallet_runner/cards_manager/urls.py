from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    #path('find/', views.find),
    re_path(r'^find/(?P<x>[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)/(?P<y>[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)/', views.get_stores_by_url),
    # регулярное выражения имеет в виду любое действительное число
]