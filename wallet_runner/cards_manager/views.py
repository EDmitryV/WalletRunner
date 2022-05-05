import json
import urllib
from urllib.request import urlopen
from rest_framework.response import Response
from rest_framework.views import APIView
from .db_logic import db_controller


class SortMyCardsView(APIView):
    def post(self, request):
        cards = []
        lat = ''
        lon = ''
        try:
            cards = request.data.get('cards')
            lat = request.data.get('latitude')
            lon = request.data.get('longitude')
        except KeyError:
            return Response({"Error": "Malformed data!"})
        places = db_controller.get_stores_in_area(lat, lon)
        if len(places) == 0:
            places = []
            for desired in ["магазин", "кафе"]:
                desired = urllib.parse.quote_plus(desired)
                url = "https://catalog.api.2gis.com/3.0/items?q=" + desired + "&fields=items.point&point=" + lat + "," \
                      + lon + "&radius=1000&sort_point=" + lat + "," + lon + "&sort=distance&key=ruugku1560"
                with urlopen(url) as response:
                    data = response.read()
                data = data.decode('utf-8')
                data = json.loads(data)
                data = data.get('result').get('items')
                places.extend(data)
            db_controller.save_new_area(latitude=lat, longitude=lon, radius=1000, stores=places)
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
        for place in results:
            name = place["name"]
            result.append(name[0:name.find(",")])
        return Response(result)
