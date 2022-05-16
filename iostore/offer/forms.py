from django.forms import ModelForm
from .models import Offer


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'
        exclude = ['host', 'final_bid', 'active', 'bid_count']
