from django.forms import ModelForm
from auctions.models import *

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'description', 'image_url', 'min_bid']

    