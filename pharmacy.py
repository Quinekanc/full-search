import sys
import requests
import helper
from io import BytesIO
from PIL import Image

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address = helper.find_obj(sys.argv[1:])

json_address = address.json()
toponym = json_address["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_a, toponym_b = [float(i) for i in toponym_coodrinates]

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f'{toponym_a},{toponym_b}',
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)

if not response:
    raise(Exception('Неправильный ввод'))

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]

point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
delta = "0.005"

map_params = {
    "ll": point,
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": f"{org_point},pm2dgl~"
          f"{toponym_a},{toponym_b},pm2dgl"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
