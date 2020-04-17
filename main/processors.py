from auction.models import Cart
import json

"""
Custom context processors
"""


def shopping_cart(request):
    """
    Returns cart data if the user is authenticated
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart()
            cart.user = request.user
        return {
            'cart': json.loads(cart.items) if cart.items else []
        }
    return {}
