# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy

from auction.forms import PlaceOrderForm
from auction.models import Product, Order, Cart, Inventory
import json
from django.views.generic.base import TemplateView
from django.conf import settings

def _transform_product_list(products: list):
    return list(map(lambda x: {
            "title": x.title,
            "price": x.price,
            "description": x.description,
            "link": f"/auction/{x.id}",
            "image": x.image.url,
            "created_at": x.created_at
        }, products))


def index(request):
    trending_product_list = Product.objects.all()
    # Get the latest 5 products
    latest_product_list = Product.objects.order_by('-created_at')[:4]

    # ! Important: Use {{ ... |safe}} to prevent character escape in the template
    context = {
        'trending_products': _transform_product_list(trending_product_list),
        'latest_products': _transform_product_list(latest_product_list),
    }
    return render(request, 'main/index.html', context)


def review_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart()
        cart.user = request.user
    cart_items = json.loads(cart.items) if cart.items else {}

    shown_list = []
    total_price = total_amount = 0
    for item_id, amount in cart_items.items():
        try:
            product = Product.objects.get(pk=int(item_id))
            if int(amount) > 0:
                subtotal = round(float(product.price) * int(amount), 2)
                to_append = {
                    'id': product.id,
                    'title': product.title,
                    'amount': amount,
                    'subtotal': "{:.2f}".format(subtotal),
                }
                total_price += subtotal
                total_amount += int(amount)

                # Check stock left, this handles out of stock items
                try:
                    inventory = Inventory.objects.get(item=product)
                    to_append.update({
                        'stock_left': inventory.stock_count
                    })
                except Inventory.DoesNotExist:
                    to_append.update({
                        'stock_left': 0
                    })

                shown_list.append(to_append)
        except Product.DoesNotExist:
            continue

    return render(request, 'main/review_order.html', {
        'cart': shown_list,
        'total_price': "{:.2f}".format(total_price),
        'total_amount': total_amount,
    })


def checkout(request):
    try:
        Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return HttpResponseBadRequest

    shipping_address = request.user.profile.shipping_address
    return render(request, 'main/checkout.html', {'shipping_address': shipping_address})

ttl_price = 0
def place_order(request):
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            cart = get_object_or_404(Cart, user=request.user)
            # Make sure we don't place an order with an empty cart
            if cart.items == "":
                raise HttpResponseBadRequest

            cart_items = json.loads(cart.items)
            order_items = []
            total_amount = total_price = 0
            # same exception handling as above
            if len(cart_items) < 1:
                raise HttpResponseBadRequest

            with transaction.atomic():
                for item_id, amount in cart_items.items():
                    product = get_object_or_404(Product, pk=int(item_id))
                    product_ivt = get_object_or_404(Inventory, item=int(item_id))
                    if product_ivt.stock_count - int(amount) < 0:
                        # Prevent transaction from committing if there's not enough stock
                        transaction.rollback()
                        # Go back to review order
                        return HttpResponseRedirect('/review-order/')
                    else:
                        product_ivt.stock_count -= int(amount)
                        product_ivt.save()

                        price = round(float(product.price) * int(amount), 2)
                        order_items.append({
                            'id': item_id,
                            'title': product.title,
                            'amount': amount,
                            'subtotal': price
                        })
                        total_amount += int(amount)
                        total_price += price

            # Save new order
            order = Order()
            order.user = request.user
            order.items = json.dumps(order_items)
            order.total_price = total_price
            ttl_price = total_price
            order.total_amount = total_amount
            order.shipping_address = form.cleaned_data['shipping_address']
            order.save()

            # Clear cart
            cart.items = json.dumps({})
            cart.save()

            # Save shipping address if requested
            print(request.POST)
            if request.POST.get('remember_address', False):
                profile = request.user.profile
                profile.shipping_address = form.cleaned_data['shipping_address']
                profile.save()

            #return HttpResponseRedirect('/order-success/')
            return HttpResponseRedirect('/payment/')

    return HttpResponseRedirect('/checkout/')



class PaymentView(TemplateView):
    template_name = 'main/payment.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['price'] = ttl_price
        return context


def order_success(request):
    return render(request, 'main/order_success.html')
