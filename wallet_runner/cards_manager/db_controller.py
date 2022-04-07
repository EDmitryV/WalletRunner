import datetime
import json
from .models import *
from .geometry import *


def find_area(attitude,longitude):
    x = float(attitude)
    y = float(longitude)

    areas = Areas.objects.all()
    
    for area in areas:
        if( is_in_area((x,y), (area.Center_atitude, area.Center_longitude), area.Radius)):
            return "You are in!"
    return "No areas :c"