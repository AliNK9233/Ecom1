
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .import models
from orders.models import Order
from .forms import OrderForm
from home.models import UserProfile,Category
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count,F,Sum
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractQuarter
import csv
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
# Create your views here.

@user_passes_test(lambda u: u.is_staff)
def admin_home(request):




    data = Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(order_count=Count('id'))
    data_amount = Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(order_amount=Sum('total_price'))

    month_labels_amount = [f'Month {entry["month"]}' for entry in data_amount]
    monthly_amount = [entry['order_amount'] for entry in data_amount]
    

    month_labels = [f'Month {entry["month"]}' for entry in data]
    monthly_values = [entry['order_count'] for entry in data]


    
    order_counts_by_status = Order.objects.annotate(
        status=F('delivery_status'),).values('status').annotate(count=Count('pk'))

    context = {
        'order_counts_by_status': order_counts_by_status,
        'month_labels' : month_labels,
        'monthly_values' : monthly_values,
        'month_labels_amount': month_labels_amount,
        'monthly_amount': monthly_amount,
       

    }
    return render(request,'admin/admin_home.html', context)
    

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

def edit_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  
        if form.is_valid():
            form.save()
            
            return redirect('admin_order_list')  
    else:
        form = OrderForm(instance=order)  # Pre-fill form for editing
    return render(request, 'admin/edit_order.html', {'form': form})



def export_orders_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write header row
    writer.writerow(['Order ID', 'User', 'Total Price', 'Order Date', 'Payment Status', 'Delivery Status', 'Payment Type'])

    # Write data rows
    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.user.username, order.total_price, order.order_date, order.payment_status, order.delivery_status, order.payment_type])

    return response


class ExportOrdersToPDF(View):
    def get(self, request, *args, **kwargs):
        # Create a response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders.pdf"'

        # Create a PDF document
        pdf_buffer = SimpleDocTemplate(response, pagesize=letter)

        # Table data
        table_data = [['Order ID', 'User', 'Total Price', 'Order Date', 'Payment Status', 'Delivery Status', 'Payment Type']]

        # Fetch orders from the database
        orders = Order.objects.all()

        # Add order data to the table
        for order in orders:
            order_data = [order.id, order.user.username, order.total_price, order.order_date, order.payment_status, order.delivery_status, order.payment_type]
            table_data.append(order_data)

        # Create a table and set styles
        order_table = Table(table_data)
        order_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Build PDF document
        pdf_buffer.build([order_table])

        return response