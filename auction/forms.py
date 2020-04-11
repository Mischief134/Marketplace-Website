from django import forms

from auction.models import Product


class CreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'image']
