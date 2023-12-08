from django.db import models

# Create your models here.

class Trade(models.Model):
    TRADE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    LONG_SHORT_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]

    symbol = models.CharField(max_length=10)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=TRADE_STATUS_CHOICES, default='open')
    long_or_short = models.CharField(max_length=29, choices=LONG_SHORT_CHOICES, default='long')
    position = models.CharField(max_length=10)
    margin = models.FloatField()
    leverage = models.FloatField()
    open_price = models.FloatField()
    current_price = models.FloatField()
    return_pnl = models.FloatField(null=True, blank=True)