from rest_framework import serializers, viewsets
from models import City


class CitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = City
		fields = ('code', 'name', 'state', 'state_abbreviation', 'vegetation_index', 'gdp')


class CityViewSet(viewsets.ModelViewSet):
	queryset = City.objects.all()
	serializer_class = CitySerializer