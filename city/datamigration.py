import utils

def migrate_data():
	city_info = None
	gdp_info = None
	try:
		city_info = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	except:
		print "Failed to open source from city info."
		return
	try:
		gdp_info = open("../pib.csv", 'r')
	except:
		print "Failed to open source from GDP info."
		return

	utils.migration_script(city_info, gdp_info)