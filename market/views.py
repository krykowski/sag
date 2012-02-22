#-*- coding: utf-8 -*-

import os
import time

from django.http import HttpResponse
from django.conf import settings
from utils import render_to
from chart.charts import ChartExt, GoogleChart

from market.models import Item, ItemHistory
from market.forms import MarketSearch

@render_to('market/index.html')
def index(request):
    result = {}
    
    if request.method == 'GET':
        form = MarketSearch()
    else:
        form = MarketSearch(request.POST)
        
        if form.is_valid():
            itemId = form.cleaned_data['items'].id
            name = form.cleaned_data['items'].name
            chartType = form.cleaned_data['chartType']
            priceType = form.cleaned_data['priceType']
            dateF = form.cleaned_data['dateF']
            dateT = form.cleaned_data['dateT']
            technology = form.cleaned_data['technology']
            
            items = ItemHistory.objects.filter(item__id=itemId)
            
            if dateF:
                items = items.filter(date__gte=dateF)
                
            if dateT:
                items = items.filter(date__lte=dateT)
                
            if technology == 'flash':
                chart = ChartExt(name, chartType)
                
                for item in items:
                    if chartType != 'candle':
                        try:
                            value = getattr(item, priceType)
                        except:
                            value = item.open
                    else:
                        value = {
                            'high': item.high,
                            'top': item.open,
                            'bottom': item.close,
                            'low': item.low,
                        }
                    
                    chart.addElement(item.item.name, value, item.date.strftime('%d.%m.%Y'))
                    
                chart.prepare()
                chart.json = chart.create()
            else:
                chart = GoogleChart(name, chartType)
                chart.addColumn('Data', 'date', 'date')
                chart.addColumn('Wartość', 'number', 'value')
                
                for item in items:
                    value = [item.date.strftime('%d.%m.%Y')]
                    
                    if chartType != 'candle':
                        try:
                            value.append(getattr(item, priceType))
                        except:
                            value.append(item.open)
                    else:
                        value.append([item.high, item.open, item.close, item.low])
                        
                    chart.addRow(value)
            
            result['chart'] = chart
    
    result['form'] = form
    
    return result
    
def parser(request):
    """
        Przykładowy content pliku do sparsowania:
        
        <TICKER>,<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
        4FUNMEDIA,20101130,17.20,17.20,15.50,15.94,24307
    """
    
    listing = os.listdir(settings.IMPORT_PATH)
    
    for fileName in listing:
        file = open(settings.IMPORT_PATH + fileName)
        
        lineNo = 0
        item = None
        
        for line in file.readlines():
            lineNo += 1
            # Omiń pierwszą linię pliku (nagłówek - <TICKER>,<DTYYYYMMDD>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>)
            if lineNo == 1:
                continue
            
            lineSplit = line.split(',')      
            
            itemData = {
                'name'  : lineSplit[0],
                'date'  : time.strftime("%Y-%m-%d", time.strptime(lineSplit[1], '%Y%m%d')),
                'open'  : lineSplit[2],
                'high'  : lineSplit[3],
                'low'   : lineSplit[4],
                'close' : lineSplit[5],
            }
            
            if item is None:
                item = Item.objects.get_or_create(name=itemData['name'])[0]
                  
            try:
                itemHistory = ItemHistory.objects.get(item=item, date=itemData['date'])
            except ItemHistory.DoesNotExist:
                itemHistory = ItemHistory(item=item, **itemData)
                itemHistory.save()
    
    return HttpResponse("Parser done")
    #return redirect('/')