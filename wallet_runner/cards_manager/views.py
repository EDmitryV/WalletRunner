import json
import urllib
from urllib.request import urlopen
from rest_framework.response import Response
from rest_framework.views import APIView
from .db_logic import db_controller


class SortMyCardsView(APIView):
    def post(self, request):
        try:
            cards = []
            for card in request.data.get('body').get('cards'):
                if card not in cards:
                    cards.append(card)
            longitude = str(request.data.get('body').get('longitude'))
            latitude = str(request.data.get('body').get('latitude'))
        except KeyError:
            return Response({"Error": "Wrong request body!"})
        places = db_controller.get_stores_in_area(latitude=latitude, longitude=longitude)
        if places is None:
            places = []
            for desired in ["магазин", "кафе"]:
                desired = urllib.parse.quote_plus(desired)
                url = "https://catalog.api.2gis.com/3.0/items?q=" + desired \
                      + "&fields=items.point&point=" + longitude \
                      + "," + latitude + "&radius=1500&sort_point=" \
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
        for card in cards:
            for place in places:
                if card in place.get('name'):
                    place['name'] = card
                    results.append(place)
                    break
        results = sorted(results, key=lambda s: abs((float(s.get('point').get('lat')) - float(latitude)))
                                                + abs((float(s.get('point').get('lon')) - float(longitude))))
        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                if results[i].get('name') == results[j].get('name'):
                    results.remove(results[j])
        response = []
        for place in results:
            response.append(place.get('name'))
        for card in cards:
            if card not in response:
                response.append(card)
        return Response(response)
