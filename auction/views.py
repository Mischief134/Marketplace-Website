from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from auction.forms import CreateForm
from auction.models import Product
from django.http import JsonResponse, HttpResponse
import json

#
# def list_of_products(request):
#     latest_product_list = Product.objects.all()
#
#     context = {'latest_product_list': latest_product_list}
#     return render(request, 'auction/productlist.html', context)


def detail(request, item_id):
    # try:
    product = get_object_or_404(Product, pk=item_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, 'auction/productdetails.html', {'product': product})


def create(request):
    if request.method == 'POST':
        form = CreateForm(json.loads(request.body))
        if form.is_valid():

            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')

            prod = Product(
                user=request.user,
                title=title, description=description, price=price, cart=None, orders=None
            )
            prod.save()

            return HttpResponse('Item added.')
        else:
            response = JsonResponse({'errors': form.errors})
            response.status_code = 400
            return response
