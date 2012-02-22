from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class ItemHistory(models.Model):
    item = models.ForeignKey(Item)
    date = models.DateField()
    
    # Prices 
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    