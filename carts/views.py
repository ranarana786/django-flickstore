from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.sessions.models import Session
from .models import Cart, CartItem
from store.models import Product, Variation

# Create your views here.

# private function make cart_id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        print('new session key has been added')
        request.session.create()
    return cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = _cart_id(request)

    try:
        cart = Cart.objects.get(cart_id=cart_id)
        print('No new cart has created', cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = cart_id
        )
        print('New cart has been created', cart)
    cart.save()

    product_variation = []

    if request.method == "POST":
        for i in request.POST:
            key = i
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass     
   
    is_cart_item_exists = CartItem.objects.filter(product=product).exists()
    if is_cart_item_exists:
         cart_item = CartItem.objects.filter(product=product)
         ex_var_list = []
         id = []
         for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

         if product_variation in ex_var_list:
                # increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
         else:
             item = CartItem.objects.create(product=product, quantity=1)
             if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                item.save()    
    else:
        try:
          cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
          cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            is_active=True
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()       
    return redirect('cart-page')

   

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.filter(product=product, cart=cart, id=cart_item_id).first()
        print(cart)
        print(product)
        print(cart_item)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart-page')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart-page')


def cart(request, total=0, quantity=0, cart_items=None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += (cart_item.quantity)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items' : cart_items
    }
    return render(request,'cart.html', context=context)

