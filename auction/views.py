from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from auction.forms import CreateForm
from auction.models import Product, Inventory
from user_app.models import User
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
    ivt = Inventory.objects.filter(item=product).values('stock_count')
    stock_count = ivt[0].get('stock_count') if len(ivt) > 0 else None
    seller = User.objects.filter(pk=product.user.id)

    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, 'auction/product_details.html', {
        'product': product,
        'stock_count': stock_count,
        'seller': seller[0],
        'pid': product.id,
        'username': request.user.username,
    })


def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            # create new product entry
            prod = form.save(commit=False)
            prod.user = request.user
            prod.save()

            # create new inventory entry associated with this product
            ivt = Inventory()
            ivt.item = prod
            ivt.save()

            return HttpResponse('Item added.')
        else:
            response = JsonResponse({'errors': form.errors})
            response.status_code = 400
            return response
