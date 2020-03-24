from django.shortcuts import render, get_object_or_404

# Create your views here.
from auction.models import Product

#
# def list_of_products(request):
#     latest_product_list = Product.objects.all()
#
#     context = {'latest_product_list': latest_product_list}
#     return render(request, 'auction/productlist.html', context)


def detail(request,id):
    # try:
    product = get_object_or_404(Product, pk=id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, 'auction/productdetails.html', {'product': product})
