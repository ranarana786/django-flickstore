from carts.models import Cart, CartItem
from carts.views import _cart_id

def cart_counter(request):
    counter = 0
    try:
        cart =Cart.objects.filter(cart_id=_cart_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart[:1])
        for _ in cart_items:
          counter += 1
    except Cart.DoesNotExist:
       counter = {}      
    
    return dict(cart_count=counter)  