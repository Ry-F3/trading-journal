from django.db import models
from django.contrib.auth.models import User

# User Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_realized_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_unrealized_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_realized_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0)


# Porfolio Tracker Model    
class PortfolioHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_realized_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    trade = models.ForeignKey('Trade', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

# Trade Journalling Model    
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
    row_number = models.IntegerField(editable=False)


    def save(self, *args, **kwargs):
        if not self.row_number:
            # Calculate row_number based on existing rows for the specific user
            existing_trade_rows = Trade.objects.filter(user=self.user).values_list('row_number', flat=True).order_by('row_number')
            existing_trade_rows = [int(row_number) for row_number in existing_trade_rows]

            # If there are existing rows, use the maximum row_number + 1
            if existing_trade_rows:
                self.row_number = max(existing_trade_rows) + 1
            else:
                # If no existing rows, start from 1
                self.row_number = 1

        super().save(*args, **kwargs)
        print(f"Saved Trade with row_number: {self.row_number}, User ID: {self.user.id}")
        print(f"Trade Details: Symbol: {self.symbol}, Status: {self.status}, Position: {self.position}, etc.")

        
        # Print the user ID and the list of rows for the user
        all_users = User.objects.all()
        for user in all_users:
            user_rows = Trade.objects.filter(user=user).values_list('row_number', flat=True).order_by('row_number')
            user_rows = [int(row_number) for row_number in user_rows]

            print(f"User ID: {user.id}, User Rows: {user_rows}")




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
        print(f"Trade Details: Symbol: {self.symbol}, Status: {self.status}, Position: {self.position}, etc.")




    def delete(self, user, *args, **kwargs):
        # Ensure that the user deleting the trade is the owner of the trade
        if self.user != user:
            raise PermissionDenied("You do not have permission to delete this trade.")

        # Get the row_number of the trade being deleted
        deleted_row_number = self.row_number

        super().delete(*args, **kwargs)
        print(f"Deleted Trade with row_number: {deleted_row_number}")

        # After deletion, re-order the remaining rows
        remaining_trades = Trade.objects.filter(user=self.user).order_by('row_number')

        for index, trade in enumerate(remaining_trades, start=1):
            trade.row_number = index
            trade.save()
            print(f"Updated Trade with row_number: {trade.row_number}")
            
    def __str__(self):
        return f"{self.symbol} - {self.row_number}"
    
class Meta:
    permissions = [
        ("delete_trade", "Can delete trades"),
    ]