# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import City
from models import CityGdpInYear
from models import AverageVegetationIndexPerYear
from serializers import CitySerializer
from serializers import AverageVegetationIndexPerYearSerializer
from serializers import CityGdpInYearSerializer
from serializers import CityViewSet
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CityList(APIView):
    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class CityDetail(APIView):
    def get_object(self, code):
        try:
            return City.objects.get(code=code)
        except City.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        city = self.get_object(code)
        serializer = CitySerializer(city)
        return Response(serializer.data)


class CityGdpInYearList(APIView):
    def get(self, request, code, format=None):
        gdp = CityGdpInYear.objects.filter(city__code=code)
        serializer = CityGdpInYearSerializer(gdp, context={'request': request}, many=True)
        return Response(serializer.data)


class CityGdpInYearDetail(APIView):
    def get_object(self, code):
        try:
            return CityGdpInYear.objects.get(city__code=code)
        except CityGdpInYear.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        gdp = self.get_object(code)
        serializer = CityGdpInYearSerializer(gdp)
        return Response(serializer.data)


class AverageVegetationIndexPerYearList(APIView):
    def get(self, request, code, format=None):
        average = AverageVegetationIndexPerYear.objects.filter(city__code=code)
        serializer = AverageVegetationIndexPerYearSerializer(average, many=True)
        return Response(serializer.data)
