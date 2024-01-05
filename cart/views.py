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

    return redirect('cart', variant.id)  # Redirect to the product details page


# def remove_from_cart(user, cart_item_id):
#     cart = Cart.objects.get(user=user)
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     cart.items.remove(cart_item)
#     cart.save()


# def update_quantity(user, cart_item_id, new_quantity):
#     cart = Cart.objects.get(user=user)
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     cart_item.quantity = new_quantity
#     cart_item.save()
#     cart.save()

# def get_cart_total(user):
#     cart = Cart.objects.get(user=user)
#     return cart.total_price
