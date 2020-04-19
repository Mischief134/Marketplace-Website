from django import forms
from django.db import models
from auction.models import Product, Order


class CreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'image']


class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address']
