from django.db import models
from django.contrib.auth.models import User

class Trade(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    LONG_SHORT_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=50)  # Explore Symbols API
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    long_short = models.CharField(max_length=5, choices=LONG_SHORT_CHOICES)
    position = models.TextField()
    margin = models.DecimalField(max_digits=10, decimal_places=2)
    leverage = models.DecimalField(max_digits=5, decimal_places=2)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    return_pnl = models.DecimalField(max_digits=10, decimal_places=2)
