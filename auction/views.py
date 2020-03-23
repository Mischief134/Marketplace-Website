from django.shortcuts import render



# Create your views here.
from auction.models import Product


def list_of_products(request):
    latest_product_list = Product.objects.all()

    context = {'latest_product_list': latest_product_list}
    return render(request, 'auction/productlist.html', context)