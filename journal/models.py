from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.core.validators import MaxLengthValidator


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
        ('long', 'long'),
        ('short', 'short'),
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
            if isinstance(self.date, str):
                self.date = datetime.strptime(self.date, '%Y-%m-%d').date()

        super().save(*args, **kwargs)
        # Print the user ID and the list of rows for the user
        all_users = User.objects.all()
        for user in all_users:
            user_rows = Trade.objects.filter(user=user).values_list('row_number', flat=True).order_by('row_number')
            user_rows = [int(row_number) for row_number in user_rows]

    def save_overwrite(self, overwrite_id, overwrite_row, edited_trade_data=None):
        """
        Overwrite the trade with the specified ID and row.

        If `edited_trade_data` is provided, update the trade with the new data.
        """
        try:
            existing_trade = Trade.objects.get(id=overwrite_id, row_number=overwrite_row)
        except Trade.DoesNotExist:
            return

        if edited_trade_data:
            for key, value in edited_trade_data.items():
                setattr(existing_trade, key, value)

        existing_trade.save()
      
    def delete(self, user, *args, **kwargs):
        # Ensure that the user deleting the trade is the owner of the trade
        if self.user != user:
            raise PermissionDenied("You do not have permission to delete this trade.")

        # Get the row_number of the trade being deleted
        deleted_row_number = self.row_number

        super().delete(*args, **kwargs)

        # After deletion, re-order the remaining rows
        remaining_trades = Trade.objects.filter(user=self.user).order_by('row_number')

        for index, trade in enumerate(remaining_trades, start=1):
            trade.row_number = index
            trade.save()
            
    def __str__(self):
        return f"{self.symbol} - {self.row_number}"
    

class Meta:
    permissions = [
        ("delete_trade", "Can delete trades"),
    ]


# Blog Post Model
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    slug = models.SlugField(max_length=20, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100, validators=[MaxLengthValidator(limit_value=20, message="Title must be 20 characters or fewer.")])
    content = models.TextField(validators=[MaxLengthValidator(limit_value=100, message="Content must be 100 characters or fewer.")])
    likes = models.ManyToManyField(User, related_name='blog_post_likes', blank=True)
    profit_loss = models.FloatField(null=True, blank=True)
    entry_price = models.FloatField(null=True, blank=True)
    exit_price = models.FloatField(null=True, blank=True)
    leverage = models.FloatField(null=True, blank=True)
    trade_type = models.CharField(max_length=255, null=True, blank=True)
    trade_image = CloudinaryField('image', default='placeholder', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.likes} -{self.title} - {self.timestamp}"
 
    def number_of_likes(self):
        return self.likes.count()



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    content = models.TextField()
    

# FAQ models
class FAQRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    question = models.TextField()
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name_plural = "FAQ Requests"
        

class AdminResponse(models.Model):
    faq_request = models.ForeignKey(FAQRequest, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
