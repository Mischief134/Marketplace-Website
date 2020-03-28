from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from auction.models import Product


class CreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()

    class Meta:
        model = Product
        fields = ['title', 'price', 'description']

    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password1', 'password2']