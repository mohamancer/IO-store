from django.forms import ModelForm
from .models import Offer
from django import forms

class OfferForm(ModelForm):
    bidding_deadline = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )
    class Meta:
        model = Offer
        fields = '__all__'
        exclude = ['host', 'final_bid', 'active', 'bid_count']

