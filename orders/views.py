from audioop import reverse
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from product_app.models import Review
from coupon_app.models import Coupon
from cart.models import Cart, UserCart
from user_app.models import Address
from .models import Order
from django.db.models import Q
from django.utils import timezone
import razorpay
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def order_list(request):
    # Retrieve all orders
    orders = Order.objects.filter(user=request.user)
    

    context = {
        'orders': orders
    }

    return render(request, 'orders/order_list.html', context)

def checkout(request):
    user = request.user
    cart = UserCart.objects.filter(Q(user=user) & Q(is_checkout_done=False))
    total_price = sum(item.sub_total for item in cart)
    addresses = Address.objects.filter(user=user)
    payment_types = ['Credit Card', 'Cash on Delivery', 'UPI']

    saved_amount = 0  # Default value for saved_amount
    applied_coupon = None  # Default value for applied_coupon

    if request.method == 'POST':
        shipping_address_id = request.POST.get('shipping_address')
        payment_type = request.POST.get('payment_type')
        coupon_code = request.POST.get('coupon_code')

        if shipping_address_id and payment_type:
            shipping_address = Address.objects.get(id=shipping_address_id)

            if coupon_code:
                coupon = get_object_or_404(Coupon, code=coupon_code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
                discount_amount = Decimal(coupon.discount_percent) / Decimal(100) * total_price
                total_price -= discount_amount

                saved_amount = discount_amount
                applied_coupon = coupon

                coupon.current_usage_count += 1
                coupon.save()

            order = Order.objects.create(
                user=user,
                total_price=total_price,
                payment_status='Pending',
                delivery_status='Pending',
                payment_type=payment_type,
                shipping_address=shipping_address,
            )

            order.cart_items.set(cart)

            # Set is_checkout_done to True for each item in the cart
            for item in cart:
                item.is_checkout_done = True
                item.save()

            return render(request, 'orders/thank_you_page.html', {'order': order, 'saved_amount': saved_amount, 'applied_coupon': applied_coupon})

    context = {'cart_items': cart, 'total_price': total_price, 'addresses': addresses, 'payment_types': payment_types}
    return render(request, 'orders/checkout.html', context)


    return render(request, 'orders/checkout.html',context )

def order_tracking(request, order_id):
    addresses = Address.objects.filter(user=request.user)
    order_obj = get_object_or_404(Order, id=order_id) 
    total_price_float = float(order_obj.total_price)
    client = razorpay.Client(auth=('rzp_test_52N7MHvpRp2r81', 'iwMO9HWPuTX5r5PT9niGWaEw'))
    #data = { "amount": order_detail.total_price, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create({ "amount": total_price_float * 100, "currency": "INR", "payment_capture": 1, })

    print('*************')
    print(payment)
    print('*************')
    
    return render(request, 'orders/order_tracking.html', {'order': order_obj, 'addresses': addresses, 'payment' : payment})



def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.delivery_status == 'Pending':
        # Implement your cancellation logic here
        order.delivery_status = 'Cancelled'
        order.save()
        return redirect('order_tracking', order_id=order_id)
    else:
        return redirect('order_tracking', order_id=order_id)

def change_address(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.delivery_status == 'Pending':
        if request.method == 'POST':
            new_address_text = request.POST.get('new_address')
            # Implement your logic to update the address here
            new_address = Address.objects.create(user=order.user, street_address=new_address_text, city='YourCity', state='YourState', zip_code='YourZipCode')
            order.shipping_address = new_address
            order.save()

        return redirect('order_tracking', order_id=order_id)
    else:
        return redirect('order_tracking', order_id=order_id)
    
def order_invoice(request, order_id):
     order = get_object_or_404(Order, id=order_id)

     context = {'order': order}
     return render(request, 'orders/invoice.html',context )

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        # Include the logic to calculate total_price
        user = request.user
        cart = UserCart.objects.filter(Q(user=user) & Q(is_checkout_done=False))
        total_price = sum(item.sub_total for item in cart)

        coupon = get_object_or_404(Coupon, code=coupon_code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())

        discounted_total = total_price - (total_price * (coupon.discount_percent / 100))

        coupon.current_usage_count += 1
        coupon.save()

        return JsonResponse({'total_amount': discounted_total})

    # Handle invalid requests or other scenarios
    return JsonResponse({'error': 'Invalid request'}, status=400)

def order_details(request, order_id):
    order_obj = get_object_or_404(Order, id=order_id) 

    items_with_reviews = []
    for item in order_obj.cart_items.all():
        variant = item.product  # Access the 'product' attribute instead of 'variant'
        review = Review.objects.filter(variant=variant, user=request.user).first()
        items_with_reviews.append({'item': item, 'review': review})

    return render(request, 'orders/order_details.html', {'order': order_obj, 'items_with_reviews': items_with_reviews})