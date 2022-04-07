from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Areas
from .db_controller import *
# Create your views here.

def index(request):
    return HttpResponse("e")

def get_stores(reques,x,y):
    out = f"{x}    {y}"

    return HttpResponse(out)