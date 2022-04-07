from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import Areas
from .db_controller import *
from cards_manager import db_controller
# Create your views here.

def index(request):
    return HttpResponse("e")

def get_stores_by_url(reques,x,y):
    #out = f"{x}    {y}"

    return HttpResponse(db_controller.find_area(x,y))