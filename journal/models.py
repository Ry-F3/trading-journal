from django.db import models, transaction
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
    position = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=10, decimal_places=2)
    leverage = models.DecimalField(max_digits=5, decimal_places=2)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    return_pnl = models.DecimalField(max_digits=10, decimal_places=2)
    row_number = models.SlugField(unique=True, editable=False)

    
    row_number = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.row_number:
            max_row = Trade.objects.aggregate(models.Max('row_number'))['row_number__max']
            max_row = int(max_row or 0)  # Convert max_row to an integer
            self.row_number = max_row + 1

        super().save(*args, **kwargs)
        print(f"Saved Trade with row_number: {self.row_number}")

def delete(self, *args, **kwargs):
    with transaction.atomic():
        # Get the row_number of the trade being deleted
        deleted_row_number = self.row_number

        super().delete(*args, **kwargs)
        print(f"Deleted Trade with row_number: {deleted_row_number}")

        # After deletion, re-order the remaining rows
        remaining_trades = Trade.objects.all().order_by('row_number')

        for index, trade in enumerate(remaining_trades, start=1):
            trade.row_number = index
            trade.save()
            print(f"Updated Trade with row_number: {trade.row_number}")

        # Update max_row after deletion
        max_row = Trade.objects.aggregate(models.Max('row_number'))['row_number__max']

        if max_row is not None:
            max_row = int(max_row)
        else:
            max_row = 0

        # If there are no remaining trades, set max_row to 0
        if max_row == deleted_row_number:
            max_row = 0

        # Set row_number for the deleted trade to the new maximum + 1
        self.row_number = max_row + 1
        self.save()
        print(f"Updated Trade with row_number: {self.row_number}")

            
    def __str__(self):
        return f"{self.symbol} - {self.row_number}"