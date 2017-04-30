from city.utils import migrate_gdp
from django.core.management.base import BaseCommand
from urllib2 import urlopen


class Command(BaseCommand):
	def handle(self, **options):
		print "Got migration"
		migrate_data()

	# def handle_noargs(self, **options):
		# print "Got migration script"


def migrate_data():
	# city_info = None
	# gdp_info = None
	# try:
	# 	city_info = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	# except:
	# 	print "Failed to open source from city info."
	# 	return
	# try:
	# 	gdp_info = open("/home/jamerson/projetos/hackathonnasa/campina/static/pib.csv", 'r')
	# except:
	# 	print "Failed to open source from GDP info."
	# 	return

	city_info = urlopen("http://api.pgi.gov.br/api/1/local/municipio.json").read()
	gdp_info = open("/home/jamerson/projetos/hackathonnasa/campina/static/pib.csv", 'r').readlines()
	migrate_gdp(city_info, gdp_info)


print "Got migration script"