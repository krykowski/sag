from django.db import models
from utils import current_time

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
    def getHistory(self):
        date = current_time()
        
        try:
            history = ItemHistory.objects.filter(date__lte=date, item=self).order_by('-date')[0]
        except IndexError:
            return None
        else:
            return history
       
    @property 
    def price(self):
        return self.getHistory().open

class ItemHistory(models.Model):
    item = models.ForeignKey(Item)
    date = models.DateField()
    
    # Prices 
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    