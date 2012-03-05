#-*- coding: utf-8 -*-
from utils import render_to
from django.contrib import messages

from investment.forms import WalletCharge, WalletItemBuy
from investment.models import Wallet, WalletItem
from django.shortcuts import redirect

@render_to('investment/wallet.html')
def wallet(request):
    PAGE_NAME = 'wallet'
    
    wallet = request.user.wallet
    
    # Distinct select based on:
    # http://stackoverflow.com/questions/4935921/django-distinct-foreign-keys
    id_list = WalletItem.objects.filter(wallet=wallet).values_list('item_id').distinct()
    items = WalletItem.objects.filter(id__in=id_list)
    
    return {
        'PAGE_NAME': PAGE_NAME,
        'wallet': wallet,
        'items': items,
    }

@render_to('investment/charge.html')
def charge(request):
    PAGE_NAME = 'charge'
    
    if request.method == 'GET':
        form = WalletCharge()
    else:
        form = WalletCharge(request.POST)
        
        if form.is_valid():
            wallet = Wallet.objects.get(user=request.user)
            wallet.charge(form.cleaned_data['value'])
            
            messages.success(request, u'Portfel został poprawnie doładowany')
            
            # Reset form values
            return redirect('investment.views.wallet')
    
    return {
        'PAGE_NAME': PAGE_NAME,
        'form': form,
    }
    
@render_to('investment/create.html')
def create(request):
    PAGE_NAME = 'action_buy'
    
    if request.method == 'GET':
        form = WalletItemBuy()
    else:
        form = WalletItemBuy(request.POST)
        
        if form.is_valid():
            wallet = Wallet.objects.get(user=request.user)
            
            if wallet.money >= int(form.cleaned_data['quantity']) * float(form.cleaned_data['price_limit']):
                wallet.add_item(form.cleaned_data['item'], form.cleaned_data['quantity'], 
                                form.cleaned_data['price_limit'], form.cleaned_data['date_limit'])
                
                messages.success(request, u'Zlecenie zakupu zostało poprawnie przyjęte.')
            else:
                messages.error(request, u'Nie posiadasz wystarcząjącej ilości środków na koncie,')
    
    return {
        'PAGE_NAME': PAGE_NAME,
        'form': form,
    }