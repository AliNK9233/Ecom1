
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import UserCart
from .models import Category,Variant,Product
from django.shortcuts import render
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt

#import forms

from .forms import SignupForm

# Create your views here.

def index(request):

    dict_cat = {
        'category':Category.objects.all(),
        'variants':Variant.objects.all()
    }
    return render(request,'index.html',dict_cat)


def product_details(request, variant_id):
    variant = get_object_or_404(Variant, pk=variant_id)
    product = variant.product
    variants = product.variant_set.all()
    return render(request, 'product_details.html', {'variant': variant, 'variants': variants, 'selected_variant': variant})



def product_by_category(request, category_id):
    variants = Variant.objects.filter(product__category=category_id).all()
    return render(request, 'products_by_category.html', {'variants': variants})



def add_to_cart(request,):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        product_check = Variant.objects.get(id=prod_id)

        if(product_check):
            if(UserCart.objects.filter(user=request.user.id,product=prod_id)):
                return JsonResponse({'status':"Product Already in Cart"})
            else:
                prod_qty = int(request.POST.get('product_qty'))
                prod_name = request.POST.get('product_name')

                if product_check.stock >= prod_qty:
                    UserCart.objects.create(user=request.user,product_id=prod_id,title=prod_name,quantity=prod_qty)
                    return JsonResponse({'status':"Product added to cart"})
                else:
                    return JsonResponse({'status':"Only"+str(product_check.stock)+"available"})
        else:
            return JsonResponse({'status':"No such product found"})
    

    return redirect('view_cart')  # Redirect to the product details page    


@csrf_exempt
def update_payment_status(request):
    print("update payment function started")
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        # Update the payment status to 'Paid'
        order = Order.objects.get(id=order_id)
        order.payment_status = 'Paid'
        order.save()

        print('*********')
        print(order_id)
        print('*********')

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

