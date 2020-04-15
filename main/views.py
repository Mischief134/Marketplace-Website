import json

from django.core import serializers
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render

from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.views import generic

from auction.models import Product


def index(request):
    latest_product_list = Product.objects.all()
    # context = {'val': "Nuri you are pidor",'latest_product_list':latest_product_list}

    # ! Important: Use {{ ... |safe}} to prevent character escape in the template
    context = {
        'trending_products': list(map(lambda x: {
            "title": x.title,
            "price": x.price,
            "description": x.description,
            "link": f"/auction/{x.id}",
            "image": x.image.url,
        }, latest_product_list))
    }
    return render(request, 'main/index.html', context)


