#-*- coding: utf-8 -*-

from django import forms

from base.forms import FormExt

from market.models import Item

class WalletCharge(FormExt):
    value = forms.DecimalField(required=True, label=u'Kwota doładowania', 
                               help_text=u'Użyj kropki jako separatora dziesiętnego.', decimal_places=2)
    
class WalletItemBuy(FormExt):
    item = forms.ModelChoiceField(Item.objects.all(), label='Instrument', initial=0)
    quantity = forms.IntegerField(label=u'Ilość akcji')
    price_limit = forms.FloatField(label='Limit cenowy', help_text=u'Maksymalna cena zakupu pojedynczej akcji.\
                                Pozostaw puste w przypadku braku limitu.', required=False)
    date_limit = forms.DateField(label='Limit czasowy', widget=forms.TextInput(attrs={'class':'datepicker_future'}),
                                 help_text=u'Okres w którym zlecenie będzie aktywne. \
                                 Pozostaw puste w przypadku braku limitu.', required=False)
        