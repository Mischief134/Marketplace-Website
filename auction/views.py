from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from auction.forms import CreateForm
from auction.models import Product, Inventory, Cart, Order
from user_app.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
import json


def detail(request, item_id):
    # try:
    product = get_object_or_404(Product, pk=item_id)
    try:
        ivt = Inventory.objects.get(item=product)
    except Inventory.DoesNotExist:
        ivt = Inventory()
        ivt.item = product
        ivt.save()
    stock_count = ivt.stock_count
    seller = User.objects.get(pk=product.user.id)

    return render(request, 'auction/product_details.html', {
        'product': product,
        'stock_count': stock_count,
        'seller': seller,
        'pid': product.id,
        'username': request.user.username,
    })


def restock(request):
    if request.method == 'POST':
        # get values from request body
        try:
            item_id = request.body['itemId']
            amount = request.body['amount']
        except ValueError:
            raise HttpResponseBadRequest

        try:
            product = Product.objects.get(pk=item_id)
        except Product.DoesNotExist:
            raise HttpResponseNotFound

        # check if the user is authorized to restock
        if product.user != request.user:
            raise HttpResponseForbidden

        try:
            inventory = Inventory.objects.get(item=item_id)
        except Inventory.DoesNotExist:
            inventory = Inventory()
            inventory.item = item_id

        inventory.stock_count += amount
        inventory.save()
        return HttpResponse('Restocked.')


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


def add_prod_to_order(request, item_id):
    try:
        orders = Order.objects.get(user_id=request.user.id)
        product = get_object_or_404(Inventory, item_id=int(item_id))
        product.stock_count -= 1
        product.save()

        if orders.items == "":
            items = {}
            new_val = 1
        else:
            items = json.loads(orders.items)
            new_val = items[str(item_id)] + 1

        items[str(item_id)] = new_val

        orders.items = json.dumps(items)
        orders.save()
        return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))

    except Cart.DoesNotExist:
        orders = Order.objects.create(user_id=request.user.id, items="", shipping_address="")
        product = get_object_or_404(Inventory, item_id=int(item_id))
        product.stock_count -= 1
        product.save()

        if orders.items == "":
            items = {}
            new_val = 1
        else:
            items = json.loads(orders.items)
            new_val = items[str(item_id)] + 1

        items[str(item_id)] = new_val

        orders.items = json.dumps(items)
        orders.save()
        return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))


def add_prod_to_cart(request, item_id):
    try:
        cart = Cart.objects.get(user_id=request.user.id)
        product = get_object_or_404(Inventory, item_id=int(item_id))
        product.stock_count -= 1
        product.save()
        print("GOTVEREN")
        # print(cart.items)

        if cart.items == "":
            items = {}
            new_val = 1
        else:
            items = json.loads(cart.items)
            new_val = items[str(item_id)] + 1

        items[str(item_id)] = new_val

        cart.items = json.dumps(items)
        cart.save()
        return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user_id = request.user.id,items="")
        product = get_object_or_404(Inventory, item_id=int(item_id))
        product.stock_count -= 1
        product.save()

        if cart.items == "":
            items = {}
            new_val = 1
        else:
            items = json.loads(cart.items)
            new_val = items[str(item_id)] + 1

        items[str(item_id)] = new_val

        cart.items = json.dumps(items)
        cart.save()
        return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))

