from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from auction.models import Product
from .forms import UserRegisterForm


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
    obj = Product.objects.get_queryset().filter(orders_id=request.user.id)
    if action is None:
        return HttpResponseRedirect('/users/profile/orders')
    elif action == 'orders':
        tab_index = 0
    elif action == 'listings':
        tab_index = 1
    else:
        raise Http404('Page does not exist')
    return render(request, 'users/profile.html', {'tabIndex': tab_index, 'orderhistory': obj})
