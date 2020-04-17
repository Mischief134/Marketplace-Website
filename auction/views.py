from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.db import transaction
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


def restock(request, item_id):
    if request.method == 'POST':
        # check if product exist
        try:
            product = Product.objects.get(pk=item_id)
        except Product.DoesNotExist:
            raise HttpResponseNotFound

        # get values from request body
        try:
            body = json.loads(request.body)
            amount = body['amount']
        except ValueError:
            raise HttpResponseBadRequest

        # check if the user is authorized to restock
        print(product.user)
        print(request.user)
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


def place_order(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            shipping_address = body['shippingAddress']
        except ValueError:
            raise HttpResponseBadRequest

        cart = get_object_or_404(Cart, user=request.user)
        # Make sure we don't place an order with an empty cart
        if cart.items == "":
            raise HttpResponseBadRequest

        cart_items = json.load(cart.items)
        # same exception handling as above
        if len(cart_items) < 1:
            raise HttpResponseBadRequest

        out_of_stock_items = []
        with transaction.atomic():
            for (item_id, amount) in enumerate(cart_items.items()):
                product_ivt = get_object_or_404(Inventory, item=int(item_id))
                if product_ivt.stock_count - int(amount) < 0:
                    out_of_stock_items.append(item_id)
                    continue
                else:
                    product_ivt.stock_count -= int(amount)
                    product_ivt.save()

            # Prevent transaction from committing if there's not enough stock
            if len(out_of_stock_items) > 0:
                transaction.rollback()
                return JsonResponse({
                    'outOfStock': out_of_stock_items
                }, status=400)

        # Save new order
        order = Order()
        order.user = request.user
        order.items = cart.items
        order.shipping_address = shipping_address
        order.save()

        return HttpResponse('Order placed.')


def add_prod_to_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart()
        cart.user = request.user
        cart.items = ""

    # Make sure we don't add out of stock items
    inventory = get_object_or_404(Inventory, item=int(item_id))
    if inventory.stock_count < 1:
        raise HttpResponseBadRequest

    if cart.items == "":
        items = {}
    else:
        items = json.loads(cart.items)

    if item_id in items:
        items[item_id] += 1
    else:
        items[item_id] = 1

    cart.items = json.dumps(items)
    cart.save()
    return HttpResponse(f"Added item {item_id} to cart.")
