import json
from urllib2 import urlopen
from models import City
from models import CityGdpInYear
from models import AverageVegetationIndexPerYear
import unicodedata
import string


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


def get_vegetation_index(city, state, begin):
	try:
		layer = "5_VEGETATION_INDEX"
		crs = "EPSG:4326"
		# time = "2016-01-01/2016-01-30"
		time = "%s-01-01/%s-01-01" % (begin, begin+1)
		resolution = "20000m"
		bbox = ','.join(get_city_bbox(city, state))
		style = "INDEX"
		bins = "32"
		maxcc = "5"
		request_url = json.loads(urlopen("http://services.sentinel-hub.com/v1/fis/b7b5e3ef-5a40-4e2a-9fd3-75ca2b81cb32?LAYER=%s&STYLE=%s&CRS=%s&TIME=%s&BBOX=%s&RESOLUTION=%s&MAXCC=%s&BINS=%s" % (layer, style, crs, time, bbox, resolution, maxcc, bins)).read())
		return request_url
	except:
		return '{}'


def get_mean_vegetation_index(json_response):
	if json_response == '{}':
		return -1
	else:
		total = 0
		for i in range(len(json_response["NDVI"])):
			total += round(json_response["NDVI"][i]["basicStats"]["mean"], 10)
		return round(total / len(json_response["NDVI"]), 16)


def get_municipios():
	json_response = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	parsed_response = json.loads(json_response)
	print parsed_response[0]
	for i in range(100):
		print "%s - %s" % (parsed_response[i]['nome'], parsed_response[i]['estado_ibge']['sigla'])


def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters)


def get_city_pib_year(city_name, state_abbreviation, year, source):
	# source = open("../pib.csv", 'r')
	result = 0
	for line in source:
		city_info = line.rstrip().split(",")
		expected_city = unicodedata.normalize('NFKD', "%s (%s)" % (city_name, state_abbreviation.upper())).encode('ascii','ignore')
		city = city_info[0]
		# print "expected city is %s and city info is %s and result is %s" % (str(expected_city), str(city_info[0]), city_info[0]==expected_city)
		if city == expected_city:
			result = city_info[year-2010]
			print result
			break
	return result



def migration_script(city_info, gdp_info):
	# json_response = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	cities = json.loads(city_info)

	for i in range(len(cities)):
		state=cities[i]['estado_ibge']['nome']
		if state == "Pernambuco":
			print "Import %s" % cities[i]
			city = City.objects.create(
				code=cities[i]['id'],
				name=cities[i]['nome'],
				state=cities[i]['estado_ibge']['nome'],
				state_abbreviation=cities[i]['estado_ibge']['sigla'])
			years = [2014, 2015, 2016]
			for year in years:
				try:
					mean = get_mean_vegetation_index(get_vegetation_index(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year))
					print mean
					vegetation_index = AverageVegetationIndexPerYear.objects.create(
						city=city,
						value=get_mean_vegetation_index(get_vegetation_index(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year)),
						year=year)
				except Exception as e:
					print e
					print mean
					print "Failed to get vegetation index of %s - %s in %d" % (cities[i]['nome'], cities[i]['estado_ibge']['nome'], year)
				try:
					gdp = CityGdpInYear.objects.create(
						city=city,
						value=get_city_pib_year(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year, gdp_info),
						year=year)
				except Exception as e:
					print e
					print "Failed to get GDP of %s - %s in %d" % (cities[i]['nome'], cities[i]['estado_ibge']['nome'], year)
				
			# print "%s - %s" % (parsed_response[i]['nome'], parsed_response[i]['estado_ibge']['sigla'])

def migrate_auxiliary_data(city_info, gdp_info):
	cities = json.loads(city_info)

	for i in range(len(cities)):
		state=cities[i]['estado_ibge']['nome']
		if state == "Pernambuco":
			print "Import %s" % cities[i]['nome']
			city = City.objects.get(
				code=cities[i]['id'])
			years = [2014, 2015, 2016]
			for year in years:
				try:
					vegetation_index = AverageVegetationIndexPerYear.objects.create(
						city=city,
						value=get_mean_vegetation_index(get_vegetation_index(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year)),
						year=year)
				except Exception as e:
					print e
					print "Failed to get vegetation index of %s - %s in %d" % (cities[i]['nome'], cities[i]['estado_ibge']['nome'], year)
				try:
					gdp = CityGdpInYear.objects.create(
						city=city,
						value=get_city_pib_year(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year, gdp_info),
						year=year)
				except Exception as e:
					print e
					print "Failed to get GDP of %s - %s in %d with GDP %d" % (cities[i]['nome'], cities[i]['estado_ibge']['nome'], year, get_city_pib_year(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year, gdp_info))


def migrate_gdp(city_info, gdp_info):
	cities = json.loads(city_info)
	for i in range(len(cities)):
		state=cities[i]['estado_ibge']['nome']
		if state == "Pernambuco":
			print "Import %s" % cities[i]['nome']
			city = City.objects.get(
				code=cities[i]['id'])
			years = [2014, 2015, 2016]
			for year in years:
				try:

					gdp = CityGdpInYear.objects.create(
						city=city,
						value=get_city_pib_year(cities[i]['nome'], cities[i]['estado_ibge']['sigla'], year, gdp_info),
						year=year)
					print get_city_pib_year(cities[i]['nome'], cities[i]['estado_ibge']['sigla'], year, gdp_info)
				except Exception as e:
					print e
					print "Failed to get GDP of %s - %s in %d with GDP %d" % (cities[i]['nome'], cities[i]['estado_ibge']['nome'], year, get_city_pib_year(cities[i]['nome'], cities[i]['estado_ibge']['nome'], year, gdp_info))