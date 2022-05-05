import json
import urllib
from urllib.request import urlopen
from rest_framework.response import Response
from rest_framework.views import APIView
from .db_logic import db_controller


class SortMyCardsView(APIView):
    def post(self, request):
        try:
            cards = request.data.get('cards')
            longitude = request.data.get('longitude')
            latitude = request.data.get('latitude')
        except KeyError:
            return Response({"Error": "Malformed data!"})
        places = db_controller.get_stores_in_area(longitude, latitude)
        if len(places) == 0:
            for desired in ["магазин", "кафе"]:
                desired = urllib.parse.quote_plus(desired)
                url = "https://catalog.api.2gis.com/3.0/items?q=" + desired \
                      + "&fields=items.point&point=" + longitude \
                      + "," + latitude + "&radius=1000&sort_point=" \
                      + longitude + "," + latitude + "&sort=distance&key=ruugku1560"
                with urlopen(url) as response:
                    data = response.read()
                data = data.decode('utf-8')
                data = json.loads(data)
                if int(data.get('meta').get('code')) != 200:
                    return Response([])
                data = data.get('result').get('items')
                places.extend(data)
            db_controller.save_new_area(latitude=latitude, longitude=longitude, radius=1000, stores=places)
        results = []
        for place in places:
            for card in cards:
                if card in place.get('name'):
                    place['name'] = card
                    results.append(place)
                    break
        for result1 in results:
            for result2 in results:
                if result1.get('name') == result2.get('name') and result1 != result2:
                    results.remove(result2)
        results = sorted(results, key=lambda s: abs((int(s.get('point').get('lat')) - float(longitude))) + abs(
            (int(s.get('point').get('lon')) - float(latitude))))
        response = []
        for place in results:
            response.append(place["name"])
        return Response(response)
