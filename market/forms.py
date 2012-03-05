#-*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from base.forms import ModelFormExt, FormExt
from market.models import Item, ItemHistory

class MarketSearch(FormExt):
    TECHNOLOGY_CHOICES = (
        ('flash', 'Flash'),
        ('js', 'JavaScript'),
    )
    
    items = forms.ModelChoiceField(Item.objects.all(), label='Instrument', required=True, initial=0)
    dateF = forms.DateField(required=False, widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder': u'Data od'}))
    dateT = forms.DateField(required=False, widget=forms.TextInput(attrs={'class':'datepicker', 'placeholder': u'Data do'}))
    chartType = forms.ChoiceField(settings.CHART_TYPES, required=True, label='Typ wykresu')
    priceType = forms.ChoiceField(settings.PRICE_TYPES, required=False, label='Cena')
    technology = forms.ChoiceField(TECHNOLOGY_CHOICES, required=True, label='Technologia')