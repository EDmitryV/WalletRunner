import requests

coordsAndCards = {'latitude': '57.916396', 'longitude': '59.973656', 'cards': ['Монетка', 'Пятёрочка', 'Магнит']}
r = requests.get('http://127.0.0.1:8000/SortMyCards', params=coordsAndCards)
r.text
