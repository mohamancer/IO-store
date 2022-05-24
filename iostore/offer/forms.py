from django.forms import ModelForm
from .models import Offer
from django import forms
from django.forms.widgets import FileInput

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

class update_address_form_offer(ModelForm):
    address = forms.CharField(max_length=250, required=True, widget = forms.HiddenInput())
    longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
    latitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())

    class Meta:
        model = Offer
        fields = ['address', 'longitude', 'latitude']