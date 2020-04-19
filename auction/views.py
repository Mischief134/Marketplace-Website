from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.db import transaction
from auction.forms import CreateForm
from auction.models import Product, Inventory, Cart
from user_app.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
import json


def detail(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    try:
        ivt = Inventory.objects.get(item=product)
    except Inventory.DoesNotExist:
        ivt = Inventory()
        ivt.item = product
        ivt.save()
    stock_count = ivt.stock_count
    seller = User.objects.get(pk=product.user.id)

    # Deduct stock count if the item is in cart
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = json.loads(cart.items)
        in_cart_item_count = int(cart_items[str(item_id)]) if str(item_id) in cart_items else 0
    except Cart.DoesNotExist:
        in_cart_item_count = 0

    return render(request, 'auction/product_details.html', {
        'product': product,
        'stock_count': stock_count,
        'in_cart': in_cart_item_count,
        'stock_left': stock_count - in_cart_item_count,
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


def add_prod_to_cart(request, item_id):
    if request.method == 'POST':
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

        amount = int(request.POST.get('amount', 1))
        if str(item_id) in items:
            amount += int(items[str(item_id)])

        items[str(item_id)] = amount

        cart.items = json.dumps(items)
        cart.save()

    return HttpResponseRedirect(f"/auction/{item_id}")


def remove_prod_from_cart(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)

        try:
            body = json.loads(request.body)
            item_id = body['itemId']
        except ValueError:
            raise HttpResponseBadRequest

        cart_items = json.loads(cart.items)
        # Remove item entirely from cart
        cart_items.pop(str(item_id))
        cart.items = json.dumps(cart_items)
        cart.save()

        return HttpResponse(f"Item {item_id} removed from cart.")
