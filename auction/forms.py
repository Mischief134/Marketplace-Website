from django import forms

from auction.models import Product, Cart


class CreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'image']


class CreateCart(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'items']
