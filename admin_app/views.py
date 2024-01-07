
from audioop import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from orders.models import Order
from home.models import UserProfile,Category
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@user_passes_test(lambda u: u.is_staff)
def admin_home(request):
    

    return render(request,'admin/admin_home.html')

@user_passes_test(lambda u: u.is_staff)
def user_management(request):

    dict_user = {
         'userdetails':UserProfile.objects.all(),
         'user':User.objects.all()
    }

    return render(request,'admin/admin_user.html',dict_user)

def activate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} has been activated.')
    return redirect('admin_home')  

def deactivate_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} has been deactivated.')
    return redirect('admin_home')

def category(request):
    
    dict_category = {
        'catgry':Category.objects.all()
    }

    return render(request,'admin/category.html',dict_category)

def add_category(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            category = Category.objects.create(
                name = name,
                description=description,
                image=image,
            )
            return redirect('category')
        
        except Exception as e:
            print(e)
            return redirect('category', {'error': 'Error creating product'})

    return render(request,'admin/add_category.html')

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            # Update the existing object
            category.name = name
            category.description = description

            if image:
                category.image = image

            category.save()

            return redirect('category')
        
        except Exception as e:
            print(e)
            return redirect('category', {'error': 'Error updating category'})

    return render(request, 'admin/edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('category')

    return render(request, 'admin/delete_category.html', {'category': category})

@staff_member_required
def admin_order_list(request):
    orders = Order.objects.all()
    delivery_status_choices = Order._meta.get_field('delivery_status').choices
    payment_status_choices = Order._meta.get_field('payment_status').choices
    context = {
        'orders': orders,
        'delivery_status_choices': delivery_status_choices,
        'payment_status_choices': payment_status_choices,
    }
    return render(request, 'admin/order_list.html', context)

@staff_member_required
def mark_as_shipped(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('_selected_action')
        Order.objects.filter(id__in=order_ids).update(delivery_status='Shipped')
        messages.success(request, 'Selected orders marked as Shipped.')
    return HttpResponseRedirect(reverse('admin:admin_order_list'))

@staff_member_required
def mark_as_delivered(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('_selected_action')
        Order.objects.filter(id__in=order_ids).update(delivery_status='Delivered')
        messages.success(request, 'Selected orders marked as Delivered.')
    return HttpResponseRedirect(reverse('admin:admin_order_list'))

@staff_member_required
def cancel_orders(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('_selected_action')
        Order.objects.filter(id__in=order_ids).update(delivery_status='Cancelled')
        messages.success(request, 'Selected orders canceled.')
    return HttpResponseRedirect(reverse('admin:admin_order_list'))



