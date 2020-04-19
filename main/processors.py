from auction.models import Cart, Product
import json

"""
Custom context processors
"""


def shopping_cart(request):
    """
    Returns cart data if the user is authenticated
    """
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart()
            cart.user = request.user
        cart_items = json.loads(cart.items) if cart.items else {}
        for item_id, amount in cart_items.items():
            try:
                Product.objects.get(pk=int(item_id))
                cart_item_count += amount
            except Product.DoesNotExist:
                continue

    return {
        'cart_item_count': cart_item_count
    }
