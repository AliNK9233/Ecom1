from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from home.models import Variant
from .models import Cart,CartItem

# Create your views here.

@login_required(login_url='login')
def view_cart(request):
    user = request.user

    # Retrieve the user's cart
    cart, created = Cart.objects.get_or_create(user=user)

    return render(request, 'cart/cart.html', {'cart': cart})


@login_required(login_url='login')
def add_to_cart(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    user = request.user

    # Check if the user already has a cart
    cart, created = Cart.objects.get_or_create(user=user)

    # Check if the variant is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(product_variant=variant)

    if not item_created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Add the item to the cart
    cart.items.add(cart_item)

    # Update the total price of the cart
    cart.total_price += variant.price
    cart.save()

    return redirect('view_cart')  # Redirect to the product details page


@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

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
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    # Increase the quantity
    cart_item.quantity += 1
    cart_item.save()

    # Update the total price
    cart = Cart.objects.get(user=request.user)
    cart.update_total_price()

    return redirect('view_cart')

def remove_from_cart(user, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    cart_item.delete()
    return redirect('view_cart')


