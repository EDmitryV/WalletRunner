import requests

coordsAndCards = {'latitude': '60.616477', 'longitude': '56.791952', 'cards': ['Монетка', 'Пятёрочка', 'Магнит']}
r = requests.get('http://127.0.0.1:8000/SortMyCards', params=coordsAndCards)
r.text
