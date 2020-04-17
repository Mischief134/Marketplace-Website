# Create your views here.
from django.shortcuts import render

from auction.models import Product


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


