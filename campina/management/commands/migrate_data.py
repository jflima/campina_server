from city.utils import migration_script
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle_noargs(self, **options):
    	print "Got migration script"


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

	migration_script(city_info, gdp_info)


print "Got migration script"