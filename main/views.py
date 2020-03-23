import json

from django.core import serializers
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404,render

from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.views import generic

# class IndeView(generic.DetailView):
#     template_name = 'index.html'
#     # context_object_name = 'value'
from auction.models import Product


def index(request):
    latest_product_list = Product.objects.all()
    # context = {'val': "Nuri you are pidor",'latest_product_list':latest_product_list}

    val = serializers.serialize("json", latest_product_list)
    # print("ADADADDA"+str(latest_product_list))
    # new_list = []
    # for x in val:
    #     print(x)
    #     # new_list.append(x['fields'])

    print("ADADADDA"+str(val))
    context = {'items_json': val}
    return render(request, 'main/index.html', context)
