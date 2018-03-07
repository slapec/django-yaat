# coding: utf-8

from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class Owner(models.Model):
    name = models.CharField(max_length=64)


class SmartItem(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    @property
    def get_total_price(self):
        return self.quantity * self.price

    @property
    def get_owner(self):
        return self.owner.name
