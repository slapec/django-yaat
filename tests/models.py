# coding: utf-8

from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
