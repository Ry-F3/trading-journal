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
    position = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=10, decimal_places=2)
    leverage = models.DecimalField(max_digits=5, decimal_places=2)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    return_pnl = models.DecimalField(max_digits=10, decimal_places=2)
    row_number = models.SlugField(unique=True, editable=False)


    def save(self, *args, **kwargs):
        if not self.row_number:
            existing_trade_rows = Trade.objects.filter(user=self.user).values_list('row_number', flat=True).order_by('row_number')
            existing_trade_rows = [int(row_number) for row_number in existing_trade_rows]

            # If there are existing rows, use the maximum row_number + 1
            if existing_trade_rows:
                self.row_number = max(existing_trade_rows) + 1
            else:
                # If no existing rows, start from 1
                self.row_number = 1

        super().save(*args, **kwargs)
        print(f"Saved Trade with row_number: {self.row_number}")


    def save_overwrite(self, overwrite_id, overwrite_row, edited_trade_data=None):
        """
        Overwrite the trade with the specified ID and row.

        If `edited_trade_data` is provided, update the trade with the new data.
        """
        try:
            existing_trade = Trade.objects.get(id=overwrite_id, row_number=overwrite_row)
        except Trade.DoesNotExist:
            print(f"Trade with ID {overwrite_id} and row {overwrite_row} does not exist.")
            return

        if edited_trade_data:
            for key, value in edited_trade_data.items():
                setattr(existing_trade, key, value)

        existing_trade.save()
        print(f"Trade overwritten successfully.")



    def delete(self, *args, **kwargs):
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
            
    def __str__(self):
        return f"{self.symbol} - {self.row_number}"