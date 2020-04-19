from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from user_app.models import Profile
from auction.models import Order, Product, ProductRating
from .forms import UserRegisterForm
import json


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, action=None):
    try:
        Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_obj = Profile()
        profile_obj.user = request.user
        profile_obj.save()

    if action is None:
        return HttpResponseRedirect('/user/profile/orders/')
    elif action == 'orders':
        tab_index = 0
    elif action == 'listings':
        tab_index = 1
    else:
        raise Http404('Page does not exist')

    order_history = Order.objects.get_queryset().filter(user=request.user)
    prods = Product.objects.select_related('inventory').filter(user=request.user)

    # Fetch item ratings
    rating_lst = ProductRating.objects.filter(item__in=list(map(lambda x: x.id, prods)))
    # Calculate rating average
    rating = {}
    for r in rating_lst:
        if rating.get(r.id):
            rating[r.id] += r.rating
        else:
            rating[r.id] = [r.rating]

    return render(request, 'users/profile.html', {
        'tabIndex': tab_index,
        'order_history': list(map(lambda x: {
            'id': x.id,
            'items': json.loads(x.items),
            'shippingAddress': x.shipping_address,
            'timePlaced': x.time_placed.strftime("%b %d %Y, %I:%M%p"),
            'totalAmount': x.total_amount,
            'totalPrice': "{:.2f}".format(x.total_price),
        }, order_history)),
        'inventory': list(map(lambda x: {
            'id': x.id,
            'title': x.title,
            'stock_count': x.inventory.stock_count,
            'rating': (sum(rating[x.id]) / len(rating[x.id])) if rating.get(x.id) else 'Not yet available'
        }, prods))
    })
