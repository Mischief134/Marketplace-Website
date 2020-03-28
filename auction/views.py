from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from auction.forms import CreateForm
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



def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()

            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')

            prod = Product(title=title,description=description,price=price,cart=None,orders=None,listed_items=request.user.id)
            prod.save()
            # messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('')
    else:
        form = CreateForm()
    return render(request, 'auction/create.html', {'form': form})
