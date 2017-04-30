# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import City
from serializers import CitySerializer
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
