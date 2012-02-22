#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User)
    money = models.FloatField()
    
class WalletItem(models.Model):
    wallet = models.ForeignKey(Wallet)
    unit_cost = models.FloatField(default=1)
    quantity = models.IntegerField()
    name = models.CharField()
    #security = models.ForeignKey()
    
    def totalCost(self):
        return self.unit_cost * self.quantity
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('B', 'Kupno'),
        ('S', 'Sprzedaż'),
    )
    
    type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    #item = models.ForeignKey()
    quantity = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    STATE_TYPES = (
        (0, 'W kolejce'),
        (1, 'Wykonana'),
        (2, 'Anulowana'),
    )
    
    state = models.IntegerField(default=0, choices=STATE_TYPES)