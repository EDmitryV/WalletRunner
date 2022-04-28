import json
import urllib
from urllib.request import urlopen

import requests
from django.http import JsonResponse, HttpResponseServerError

from .db_logic import db_controller


def sort_my_cards(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            cards = []
            for card in json_data.get('cards'):
               cards.append(card)
            lat = request.GET.get('latitude')
            lon = request.GET.get('longitude')
        except KeyError:
            HttpResponseServerError("Malformed data!")
        places = db_controller.get_stores_in_area(lat, lon)
        if len(places) == 0:
            places = []
            for type in ["магазин", "кафе"]:
                type = urllib.parse.quote_plus(type)
                url = "https://catalog.api.2gis.com/3.0/items?q=" + type + "&fields=items.point&point=" + lat + "," + lon + "&radius=10000&sort_point=" + lat + "," + lon + "&sort=distance&key=ruugku1560"
                with urlopen(url) as response:
                    data = response.read()
                data = data.decode('utf-8')
                data = json.loads(data)
                data = data.get('result').get('items')
                places.extend(data)
            db_controller.save_new_area(latitude=lat, longitude=lon, radius=10000, stores=places)
        results = []
        for s in places:
            if cards.__contains__(s.get('name').split(',')[0]):
                results.append(s)
        for s1 in results:
            for s2 in results:
                if s1.get('name') == s2.get('name') and s1 != s2:
                    results.remove(s2)
        results = sorted(results, key=lambda s: abs((int(s.get('point').get('lat')) - float(lat))) + abs(
            (int(s.get('point').get('lon')) - float(lon))))
        result = []
        for store in results:
            name = store["name"]
            result.append(name[0:name.find(",")])
        return JsonResponse(json.dumps(result), safe=False)
    return JsonResponse()
    # cards = request.GET.getlist('cards')
    # lat = request.GET.get('latitude')
    # lon = request.GET.get('longitude')
    # places = db_controller.get_stores_in_area(lat, lon)
    # if len(places) == 0:
    #     places = []
    #     for type in ["магазин", "кафе"]:
    #         type = urllib.parse.quote_plus(type)
    #         url = "https://catalog.api.2gis.com/3.0/items?q=" + type + "&fields=items.point&point="+lat+","+lon+"&radius=10000&sort_point="+lat+","+lon+"&sort=distance&key=ruugku1560"
    #         with urlopen(url) as response:
    #             data = response.read()
    #         data = data.decode('utf-8')
    #         data = json.loads(data)
    #         data = data.get('result').get('items')
    #         places.extend(data)
    #     db_controller.save_new_area(latitude=lat, longitude=lon, radius=10000, stores=places)
    # results = []
    # for s in places:
    #     if cards.__contains__(s.get('name').split(',')[0]):
    #         results.append(s)
    # for s1 in results:
    #     for s2 in results:
    #         if s1.get('name') == s2.get('name') and s1 != s2:
    #             results.remove(s2)
    # results = sorted(results, key=lambda s: abs((int(s.get('point').get('lat')) - float(lat))) + abs((int(s.get('point').get('lon')) - float(lon))))
    # result = []
    # for store in results:
    #     name = store["name"]
    #     result.append(name[0:name.find(",")])
    # return JsonResponse(json.dumps(result), safe=False)
