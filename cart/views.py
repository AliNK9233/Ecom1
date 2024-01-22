from decimal import Decimal
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from home.models import Variant
from .models import Cart,CartItem,UserCart

# Create your views here.

@login_required(login_url='login')
def view_cart(request):
    user = request.user

    # Retrieve the user's cart
    cart= UserCart.objects.filter(Q(user=user) & Q(is_checkout_done=False))

    cart_total = sum(Decimal(item.sub_total) for item in cart)

    context =  {'cart_items': cart,'total':cart_total}

    return render(request, 'cart/cart.html', context)


@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(UserCart, id=cart_item_id)

    # Decrease the quantity, but ensure it doesn't go below 1
    cart_item.quantity = max(0, cart_item.quantity - 1)
    cart_item.save()

    # If the quantity becomes zero, remove the item from the cart
    if cart_item.quantity == 0:
        cart_item.delete()

    # Update the total price
    cart = Cart.objects.get(user=request.user)
    cart.update_total_price()

    return redirect('view_cart')

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(UserCart, id=cart_item_id)
    
    # Increase the quantity
    cart_item.quantity += 1
    cart_item.save()

    # Update the total price
    cart = Cart.objects.get(user=request.user)
    cart.update_total_price()

    return redirect('view_cart')

def remove_from_cart(user, cart_item_id):
    cart_item = get_object_or_404(UserCart, id=cart_item_id)
    
    cart_item.delete()
    return redirect('view_cart')


