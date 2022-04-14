import datetime
import json
from tkinter import NE
# from wallet_runner.cards_manager.models import *
# from .geometry import *

# по координатам вернуть все орг-ии в зоне, к которой относится точка (список)
from .geometry import is_in_area
from ..models import Areas, Area_Store, Networks, Stores


def get_stores_in_area(latitude, longitude):
    x = float(latitude)
    y = float(longitude)
    areas = Areas.objects.all()
    user_area_id = -1
    for area in areas:
        if( is_in_area((x,y), (area.Center_latitude, area.Center_longitude), area.Radius)):
            user_area_id = area.Area_id
            print(user_area_id)
            break

    if user_area_id == -1:
        # get_api(x,y)
        # где-то тут сохранение зоны
        # user_area_id должно быть присвоено
        return []
    
    user_area_stores = Area_Store.objects.filter(Area_id = user_area_id)
    res = []
    for area_store in user_area_stores:
        store =area_store.Store_id
        dct = {
            'id':store.Store_id,
            'point':{
                'lat':store.Store_latitude,
                'lon':store.Store_longitude,
            },
            'name':store.Network_id.Network_name
        }
        res.append(dct)
    return res
    #user_area_stores[0] # нужно протестировать возврат

        

# через список словарей с инфой о магазинах создать зону и запихать ее в базу
def save_new_area(latitude, longitude, radius, stores):
        areas = Areas.objects.all()
        area_id = areas.count()
        new_area = Areas()
        new_area.Area_id = area_id
        new_area.Center_latitude = latitude
        new_area.Center_longitude = longitude
        new_area.Radius = radius 
        new_area.Creation_date = datetime.date.today()
        new_area.Is_Active = True

        new_area.save()


        for store in stores:
            new_store = Stores()
            new_store.Store_id = store["id"]
            new_store.Store_latitude = store['point']["lat"]
            new_store.Store_longitude = store['point']["lon"]
            network = store["name"]
            if Networks.objects.filter(Network_name = store['name']).count() == 0:
                new_network = Networks()
                new_network.Network_id = Networks.objects.all().count()
                new_network.Network_name = store['name']
                new_network.save()

            new_store.Network_id = Networks.objects.filter(Network_name = store['name'])[0]
            new_store.save()


            area_store = Area_Store()
            area_store.Area_id = new_area
            area_store.Store_id = new_store
            area_store.save()
        
        return

