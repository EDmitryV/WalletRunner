import json

from django.http import JsonResponse

from .db_logic import db_controller


def sort_my_cards(request):
    cards = request.GET.getlist('cards')
    lat = request.GET.get('latitude')
    lon = request.GET.get('longitude')
    # data = db_controller.get_stores_in_area(lat, lon)
    data = []
    if len(data) == 0:
        #catalog.api.2gis.com/3.0/items?q=кафе&fields=items.point&point=60.598759,56.802272&radius=10000&sort_point=60.598759,56.802272&sort=distance&key=ruugku1560
        # params = {'q': 'магазин',
        #           'fields': 'items.point',
        #           'point': lon + ',' + lat,
        #           'radius': '10000',
        #           'sort_point': lon + ',' + lat,
        #           'sort': 'distance',
        #           'key': 'ruugku1560'}
        # r = requests.get('https://catalog.api.2gis.com/3.0/items', params=params)
        # data = json.JSONDecoder.decode(r.text)
        data = json.loads('{"meta":{"api_version":"3.0.783441","code":200,"issue_date":"20220414"},'
                                       '"result":{"items":[{"address_comment":"1 этаж","address_name":"Учительская, '
                                       '12","id":"70000001020967194","name":"Пятёрочка, сеть магазинов",'
                                       '"point":{"lat":57.916447,"lon":59.972782},"type":"branch"},'
                                       '{"address_comment":"вход через магазин Пятёрочка",'
                                       '"address_name":"Учительская, 12","id":"70000001040821885","name":"Ореховый '
                                       'рай, магазин","point":{"lat":57.916447,"lon":59.972782},"type":"branch"},'
                                       '{"address_name":"Циолковского, 21","id":"70000001059290249",'
                                       '"name":"Табакерка, г. Нижний Тагил","point":{"lat":57.917078,'
                                       '"lon":59.971442},"type":"branch"},{"address_comment":"цокольный этаж",'
                                       '"address_name":"Газетная, 97а","id":"70000001040946371","name":"Территория '
                                       'мебели, магазин","point":{"lat":57.914743,"lon":59.975909},"type":"branch"},'
                                       '{"address_name":"Газетная, 95","id":"70000001060102512","name":"Пятёрочка, '
                                       'сеть магазинов","point":{"lat":57.91421,"lon":59.974377},"type":"branch"},'
                                       '{"address_name":"Газетная, 95","id":"6333715256970799","name":"Монетка, '
                                       'торговая сеть","point":{"lat":57.914117,"lon":59.974083},"type":"branch"},'
                                       '{"address_comment":"1 этаж","address_name":"Газетная, 97а",'
                                       '"id":"70000001019422584","name":"Магнит, сеть супермаркетов",'
                                       '"point":{"lat":57.91443,"lon":59.976162},"type":"branch"},'
                                       '{"address_comment":"1 этаж","address_name":"Газетная, 97а",'
                                       '"id":"70000001027493324","name":"Полюс торг","point":{"lat":57.91445,'
                                       '"lon":59.97635},"type":"branch"},{"address_comment":"1 этаж",'
                                       '"address_name":"Газетная, 97а","id":"70000001024028168","name":"Табакерка, '
                                       'магазин","point":{"lat":57.914463,"lon":59.976478},"type":"branch"},'
                                       '{"address_name":"Газетная, 97а","id":"70000001040450032","name":"Мясной '
                                       'выбор, магазин","point":{"lat":57.914463,"lon":59.976478},"type":"branch"}],'
                                       '"total":743}}')
        data = data.get('result').get('items')
        # db_controller.save_new_area(latitude=lat, longitude=lon, radius=10000, stores=stores)
        # filtered_ls = filter(lambda s: cards.__contains__(s.get('name').split(',')[0]), stores)
    stores = []
    for s in data:
        if cards.__contains__(s.get('name').split(',')[0]):
            stores.append(s)
    for s1 in stores:
        for s2 in stores:
            if s1.get('name') == s2.get('name') and s1 != s2:
                stores.remove(s2)
    stores = sorted(stores, key=lambda s: abs((int(s.get('point').get('lat')) - float(lat))) + abs((int(s.get('point').get('lon')) - float(lon))))
    result = []
    for store in stores:
        name = store["name"]
        result.append(name[0:name.find(",")])
    return JsonResponse(json.dumps(result), safe=False)
