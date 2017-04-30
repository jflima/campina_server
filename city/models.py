# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class City(models.Model):
	code = models.CharField(max_length=6, default="")
	name = models.CharField(max_length = 50)
	state = models.CharField(max_length = 20)
	state_abbreviation = models.CharField(max_length = 2)


class CityGdpInYear(models.Model):
	city = models.ForeignKey(City)
	year = models.IntegerField()
	value = models.DecimalField(max_digits=13, decimal_places=2, default=0.0)


class AverageVegetationIndexPerYear(models.Model):
	city = models.ForeignKey(City)
	value = models.DecimalField(max_digits = 18, decimal_places=16)
	year = models.IntegerField()
