import json
from urllib2 import urlopen
from models import City


def get_city_bbox(city, state):
	json_response = urlopen("http://nominatim.openstreetmap.org/search?q=%s+%s&format=json" % (city, state)).read()
	parsed = json.loads(json_response)
	return parsed[0]["boundingbox"]


def get_polygon(city, state):
	json_response = urlopen("http://nominatim.openstreetmap.org/search?q=%s+%s&format=json" % (city, state)).read()
	parsed = json.loads(json_response)
	code = parsed[0]["osm_id"]
	response = urlopen("http://polygons.openstreetmap.fr/get_wkt.py?id=%s&params=0" % (code)).read()
	return response.split(";")[1].rstrip()


def get_vegetation_index(city, state):
	layer = "5_VEGETATION_INDEX"
	crs = "EPSG:4326"
	time = "2016-01-01/2016-01-30"
	resolution = "1000m"
	bbox = ','.join(get_city_bbox(city, state))
	style = "INDEX"
	bins = "32"
	maxcc = "5"
	request_url = urlopen("http://services.sentinel-hub.com/v1/fis/b7b5e3ef-5a40-4e2a-9fd3-75ca2b81cb32?LAYER=%s&STYLE=%s&CRS=%s&TIME=%s&BBOX=%s&RESOLUTION=%s&MAXCC=%s&BINS=%s" % (layer, style, crs, time, bbox, resolution, maxcc, bins)).read()
	return request_url


def get_mean_vegetation_index(json_response):
	total = 0
	for i in json_response["NDVI"]:
		total += json_response["NDVI"][i]["basicStats"]["mean"]
	return total / len(json_response["NDVI"])


def get_municipios():
	json_response = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	parsed_response = json.loads(json_response)
	print parsed_response[0]
	for i in range(100):
		print "%s - %s" % (parsed_response[i]['nome'], parsed_response[i]['estado_ibge']['sigla'])


def migration_script():
	json_response = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	cities = json.loads(json_response)
	for i in range(len(cities)):
		City.objects.create(
			code=cities[i]['id'],
			name=cities[i]['nome'],
			state=cities[i]['estado_ibge'],
			state_abbreviation=cities[i]['estado_ibge']['sigla'],
			vegetation_index=get_vegetation_index(cities[i]['nome'], cities[i]['estado_ibge']))
		print "%s - %s" % (parsed_response[i]['nome'], parsed_response[i]['estado_ibge']['sigla'])
