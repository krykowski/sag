#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from market.models import Item
import utils
import datetime

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User)
    money = models.FloatField()
    
    def charge(self, amount):
        t = Transaction()
        t.type = 'C'
        t.quantity = 1
        t.description = u'Doładowanie portfela inwestycyjnego'
        t.state = 1
        t.value = float(amount)
        t.user = self.user
        t.save()
        
    def add_item(self, item, quantity, pLimit, dLimit):
        t = Transaction()
        t.type = 'B'
        t.item = item
        t.quantity = quantity
        t.description = 'Zakup akcji %s' % (item.name)
        t.state = 1
        t.user = self.user
        
        if pLimit is not None:
            t.price_limit = pLimit
            
        if dLimit is not None:
            t.date_limit = dLimit
        
        t.save()
    
class WalletItem(models.Model):
    wallet = models.ForeignKey(Wallet)
    unit_cost = models.FloatField(default=1)
    quantity = models.IntegerField()
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item)
    created = models.DateTimeField(auto_now_add=True)
    
    def totalCost(self):
        return self.unit_cost * self.quantity
    
    def average_buy_price(self):
        items = WalletItem.objects.filter(item=self.item)
        
        count = 0
        cost = 0
        
        for item in items:
            cost += item.totalCost()
            count += item.quantity
            
        return cost / count
    
    def total_buy_price(self):
        items = WalletItem.objects.filter(item=self.item)
        
        cost = 0
        
        for item in items:
            cost += item.totalCost()
            
        return cost
    
    def quantity_total(self):
        items = WalletItem.objects.filter(item=self.item)
        
        count = 0
        for item in items:
            count += item.quantity
            
        return count
    
    def current_value(self):
        return self.item.price * self.quantity_total()
    
    def oldest(self):
        return WalletItem.objects.filter(item=self.item).order_by('-created')[0]
    
    def profit(self):
        return self.current_value() - self.total_buy_price()
    
    def save(self, force_insert=False, force_update=False, using=None):
        is_new = False
        if not self.id:
            is_new = True
            
        result = super(WalletItem, self).save(force_insert, force_update, using)
        
        if is_new:
            self.created = utils.current_time().date()
        
        return result
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('C', 'Doładowanie'),
        ('B', 'Kupno'),
        ('S', 'Sprzedaż'),
    )
    
    type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    item = models.ForeignKey(Item, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    
    # For buying-selling purpose
    price_limit = models.FloatField(null=True, blank=True)
    date_limit = models.DateField(null=True, blank=True)
    
    STATE_TYPES = (
        (0, 'W kolejce'),
        (1, 'Wykonana'),
        (2, 'Anulowana'),
    )
    
    state = models.IntegerField(default=0, choices=STATE_TYPES)
    
    def save(self, force_insert=False, force_update=False, using=None):
        is_new = False
        if not self.id:
            is_new = True
            
        result = super(Transaction, self).save(force_insert, force_update, using)
        
        if is_new:
            self.created = utils.current_time().date()
            
        self.updated = utils.current_time().date()
        
        if self.state != 1:
            return result
        
        if self.type == 'C':
            self.__chargeWallet()
        elif self.type == 'B':
            if self.check_buy_conditions():
                self.__addWalletItem()
        elif self.type == 'S':
            self.__sellWalletItem()
        
        return result
    
    def check_buy_conditions(self):
        date = utils.current_time().date()
        price = self.item.price
        
        if (self.date_limit and self.date_limit < date) or (self.price_limit and self.price_limit < price):
            return False
        
        return True
    
    def __chargeWallet(self):
        wallet = Wallet.objects.get(user=self.user)
        wallet.money += self.value
        wallet.save()
        
    def __addWalletItem(self):
        item = WalletItem()
        item.wallet = Wallet.objects.get(user=self.user)
        item.item = self.item  
        item.unit_cost = self.item.price
        item.quantity = self.quantity
        item.name = self.item.name
        item.save()
        
    def __sellWalletItem(self):
        item = WalletItem.objects.filter(wallet=self.user.wallet, item=self.item)
        pass #fixme todo. Jak zrobic system, ktory zachowa srednia wartosc zakupu jednostki ?
    