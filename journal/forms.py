from django import forms
from .models import Trade

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


        # Set choices for 'status' and 'long_short' fields
        self.fields['status'].choices = Trade.STATUS_CHOICES
        self.fields['long_short'].choices = Trade.LONG_SHORT_CHOICES

    def clean(self):
        cleaned_data = super().clean()
        # Add additional cleaning logic if needed
        return cleaned_data

