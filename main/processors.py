from auction.models import Cart, Product
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
        cart_items = json.loads(cart.items) if cart.items else {}
        shown_list = []
        for item_id, amount in cart_items.items():
            try:
                product = Product.objects.get(pk=int(item_id))
                if int(amount) > 0:
                    shown_list.append({
                        'id': product.id,
                        'title': product.title,
                        'amount': amount
                    })
            except Product.DoesNotExist:
                continue

        return {
            'cart': shown_list
        }
    return {}
