import datetime

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone

from auction.forms import CreateForm, CreateCart
from auction.models import Product, Inventory, Cart, Order
from user_app.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
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

def restock(request,item_id, amount):

    product = get_object_or_404(Inventory, item_id=int(item_id))
    if product.user.id == request.user.id :
        product.stock_count += amount
        product.save()
        return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))

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

def edit_order(request,item_id):
    product = get_object_or_404(Product, item_id=int(item_id))
    if request.method == 'POST':
        product.title = request.POST['title']
        product.price= int(request.POST['price'])
        product.description= (request.POST['description'])
        product.image = request.POST['image']
        # return redirect(request.META['HTTP_REFERER'])
        return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))

def add_prod_to_order(request,item_id):
    try:
        orders = Order.objects.get(user_id=request.user.id)
        product = get_object_or_404(Inventory, item_id=int(item_id))


        if product.stock_count > 0:
            product.stock_count -= 1
            product.save()

            iden = str(item_id)
            if orders.items == "":
                dict = {}
                dict[iden] = 0
            else:
                dict = json.loads(orders.items)
                dict[iden] = 0

            dict[iden] += 1



            orders.items = json.dumps(dict)
            orders.save()
            return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
        else:
            return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
            # return redirect(request.META['HTTP_REFERER'])


    except Order.DoesNotExist:

        orders = Order.objects.create(user_id=request.user.id, items="",shipping_address="",time_placed = timezone.now())
        product = get_object_or_404(Inventory, item_id=int(item_id))


        if product.stock_count > 0:
            product.stock_count -= 1
            product.save()


            iden = str(item_id)
            if orders.items == "":
                dict = {}
                dict[iden] = 0
            else:
                dict = json.loads(orders.items)
                dict[iden] = 0

            dict[iden] += 1

            # dict[iden]= new_val

            orders.items = json.dumps(dict)
            orders.save()
            return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
        else:
            return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
            # return redirect(request.META['HTTP_REFERER'])


def add_prod_to_cart(request, item_id):

        try:
            cart = Cart.objects.get(user_id=request.user.id)
            product = get_object_or_404(Inventory, item_id=int(item_id))
            if product.stock_count >0:




                iden = str(item_id)
                if cart.items =="":
                    dict = {}
                    dict[iden] = 0
                else:
                    dict = json.loads(cart.items)
                    dict[iden] = 0

                dict[iden] += 1


                # dict[iden]= new_val

                cart.items =json.dumps(dict)
                cart.save()
                return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
            else:
                return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
                # return redirect(request.META['HTTP_REFERER'])


        except Cart.DoesNotExist:


            cart = Cart.objects.create(user_id = request.user.id,items="")
            product = get_object_or_404(Inventory, item_id=int(item_id))
            # product.stock_count -= 1
            # product.save()
            if product.stock_count >0:

                # product.stock_count -= 1
                # product.save()
                # print("GOTVEREN")
                # print(cart.items)


                iden = str(item_id)
                if cart.items =="":
                    dict = {}
                    dict[iden] = 0
                else:
                    dict = json.loads(cart.items)
                    dict[iden] = 0

                dict[iden] += 1


                # dict[iden]= new_val

                cart.items =json.dumps(dict)
                cart.save()
                return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
            else:
                return HttpResponseRedirect(reverse('auction:detail', args=(item_id,)))
                # return redirect(request.META['HTTP_REFERER'])

