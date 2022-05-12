import json
import urllib
from collections import OrderedDict
from urllib.request import urlopen
from rest_framework.response import Response
from rest_framework.views import APIView
from .db_logic import db_controller


class SortMyCardsView(APIView):
    def post(self, request):
        try:
            cards = OrderedDict()
            for card in request.data.get('body').get('cards'):
                if card not in cards:
                    cards[card] = 1
                else:
                    cards[card] += 1
            longitude = str(request.data.get('body').get('longitude'))
            latitude = str(request.data.get('body').get('latitude'))
        except KeyError:
            return Response({"Error": "Wrong request body!"})
        places = db_controller.get_stores_in_area(longitude, latitude)
        if places is None:
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
            db_controller.save_new_area(latitude=latitude, longitude=longitude, radius=1500, stores=places)
        results = []
        for card in cards.keys():
            for place in places:
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
            for i in range(cards[place["name"]]):
                response.append(place["name"])
        for place in cards.keys():
            if place not in response:
                for i in range(cards[place]):
                    response.append(place)
        return Response(response)
