from django import forms
from .models import Trade, BlogPost, Comment  

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        exclude = ['user']
        fields = '__all__'
        # widgets = {'id': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__(*args, **kwargs)
            
        self.fields['symbol'].widget = forms.TextInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Symbol'})
        self.fields['date'].widget = forms.DateInput(attrs={'class':  'form-control form-control-sm', 'type': 'date'})
        self.fields['status'].widget = forms.Select(attrs={'class':  'form-control form-control-sm'})
        self.fields['long_short'].widget = forms.Select(attrs={'class':  'form-control form-control-sm'})
        self.fields['position'].widget = forms.NumberInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Position'})
        self.fields['margin'].widget = forms.NumberInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Margin'})
        self.fields['leverage'].widget = forms.NumberInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Leverage'})
        self.fields['open_price'].widget = forms.NumberInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Open Price'})
        self.fields['current_price'].widget = forms.NumberInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Current Price'})
        self.fields['return_pnl'].widget = forms.NumberInput(attrs={'class':  'form-control form-control-sm', 'placeholder': 'Enter Return PnL'})
        
        self.fields['open_price'].widget.attrs['step'] = 'any'  # Allow any step value
        self.fields['open_price'].widget.attrs['min'] = 0  # Set the minimum allowed value if needed
        self.fields['open_price'].widget.attrs['max'] = 1000000000000  # Set the maximum allowed value if needed

        self.fields['margin'].widget.attrs['step'] = 'any'  # Allow any step value
        self.fields['margin'].widget.attrs['min'] = 0  # Set the minimum allowed value if needed
        self.fields['margin'].widget.attrs['max'] = 100000000000000  # Set the maximum allowed value if needed

        self.fields['current_price'].widget.attrs['step'] = 'any'  # Allow any step value
        self.fields['current_price'].widget.attrs['min'] = 0  # Set the minimum allowed value if needed
        self.fields['current_price'].widget.attrs['max'] = 10000000000  # Set the maximum allowed value if needed

        self.fields['return_pnl'].widget.attrs['step'] = 'any'  # Allow any step value
        self.fields['return_pnl'].widget.attrs['min'] = -1000000000000  # Set the minimum allowed value if needed
        self.fields['return_pnl'].widget.attrs['max'] = 10000000000000  #

        # Set choices for 'status' and 'long_short' fields
        self.fields['status'].choices = Trade.STATUS_CHOICES
        self.fields['long_short'].choices = Trade.LONG_SHORT_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        # Add additional cleaning logic if needed
        return cleaned_data
    
class PortfolioBalanceForm(forms.Form):
    portfolio_balance = forms.DecimalField(
        label='Enter your desired amount:',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Update your Balance e.g $1,000',
                'step': 'any',  # Allow any step value
                'min': 0,       # Set the minimum allowed value
                'max': 1000000000000,  # Set the maximum allowed value if needed
            }
        ),
        min_value=0,  # Set the minimum allowed value
        max_value=1000000000000,  # Set the maximum allowed value if needed
        required=True
    )
    

class TradeFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retrieve distinct symbols from the Trade model
        symbols = Trade.objects.values_list('symbol', flat=True).distinct()

        # Add a choice for each symbol, and an option for 'All'
        symbol_choices = [('', 'All')] + [(symbol, symbol) for symbol in symbols]
        self.fields['symbol_filter'] = forms.ChoiceField(choices=symbol_choices, required=False)

        self.fields['date_filter'] = forms.ChoiceField(choices=[
            ('', 'Any date'),
            ('today', 'Today'),
            ('past_7_days', 'Past 7 days'),
            ('this_month', 'This month'),
            ('this_year', 'This year'),
        ], required=False)

        # Additional fields for custom date range
        self.fields['custom_date_start_month'] = forms.IntegerField(required=False)
        self.fields['custom_date_start_day'] = forms.IntegerField(required=False)
        self.fields['custom_date_start_year'] = forms.IntegerField(required=False)

        long_short_choices = [
            ('', 'All'),
            ('long', 'long'),
            ('short', 'short'),
        ]

        self.fields['long_short_filter'] = forms.ChoiceField(choices=long_short_choices, required=False)

        pnl_choices = [
            ('', 'All'),
            ('profit', 'Profit'),
            ('loss', 'Loss'),
        ]

        self.fields['pnl_filter'] = forms.ChoiceField(choices=pnl_choices, required=False)
        
class BlogPostForm(forms.ModelForm):
    profit_percentage = forms.FloatField(required=False)
    profit_loss = forms.FloatField(required=False)
    entry_price = forms.FloatField(required=False)
    exit_price = forms.FloatField(required=False)
    leverage = forms.FloatField(required=False)
    trade_type = forms.CharField(max_length=255, required=False)
    trade_image = forms.ImageField(required=False)
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'timestamp', 'likes', 'profit_loss', 'entry_price', 'exit_price', 'leverage', 'trade_type', 'trade_image']
        widgets = {
                'timestamp': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'required': False}),
                'profit_loss': forms.HiddenInput(),
                'entry_price': forms.HiddenInput(),
                'exit_price': forms.HiddenInput(),
                'leverage': forms.HiddenInput(),
                'trade_type': forms.HiddenInput(),
        }
        
        labels = {
            'title': 'Post Title',
            'content': 'Content',
            'timestamp': 'Timestamp',
            'likes': 'Likes',
            'profit_loss': 'Profit/Loss',
            'entry_price': 'Entry Price',
            'exit_price': 'Exit Price',
            'leverage': 'Leverage',
            'trade_type': 'Trade Type',
            'trade_image': 'Trade Image',
        }
        required = {
            'title': True,
            'content': True,
            'likes': False,  
            'profit_loss': False,  
            'entry_price': False,  
            'exit_price': False,  
            'leverage': False,  
            'trade_type': False,  
            'trade_image': True,
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['timestamp'].widget = forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']        