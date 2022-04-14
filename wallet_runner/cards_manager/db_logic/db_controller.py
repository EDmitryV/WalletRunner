import datetime
import json
from ..models import *
from .geometry import *

# по координатам вернуть все орг-ии в зоне, к которой относится точка (список)

def get_stores_in_area(attitude,longitude):
    x = float(attitude)
    y = float(longitude)
    areas = Areas.objects.all()
    user_area_id = -1
    for area in areas:
        if( is_in_area((x,y), (area.Center_atitude, area.Center_longitude), area.Radius)):
            user_area_id = area.Area_id
            break

    
    if user_area_id == -1:
        # get_api(x,y)
        # где-то тут сохранение зоны
        # user_area_id должно быть присвоено
        pass
    
    user_area_stores = Area_Store.objects.get(Area_id = user_area_id)
    return user_area_stores # нужно протестировать возврат

        

# через список словарей с инфой о магазинах создать зону и запихать ее в базу
def save_new_area(x,y,radius,stores):
        areas = Areas.objects.all()
        area_id = areas.count

        new_area = Areas()
        new_area.Area_id = area_id
        new_area.Center_atitude = x
        new_area.Center_longitude = y
        new_area.Radius = radius 
        new_area.Creation_date = datetime.date.today()
        new_area.Is_Active = True

        new_area.save()



        for store in stores:
            new_store = Stores()
            new_store.Store_id = store["id"]
            new_store.Store_atitude = store["atitude"]
            new_store.Store_longitude = store["longitude"]
            new_store.Network_id = store["network"]
            new_store.save()


            area_store = Area_Store()
            area_store.Area_id = area_id
            area_store.Store_id = new_store.Store_id
            area_store.save()
        
        return

