from rest_framework import serializers, viewsets
from models import City
from models import CityGdpInYear
from models import AverageVegetationIndexPerYear


class CitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = City
		fields = ('code', 'name', 'state', 'state_abbreviation')


class CityViewSet(viewsets.ModelViewSet):
	queryset = City.objects.all()
	serializer_class = CitySerializer


class CityGdpInYearSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = CityGdpInYear
		fields = ('value', 'year')


class AverageVegetationIndexPerYearSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = AverageVegetationIndexPerYear
		fields = ('value', 'year')


class CityViewSet(viewsets.ModelViewSet):
	queryset = City.objects.all()
	serializer_class = CitySerializer