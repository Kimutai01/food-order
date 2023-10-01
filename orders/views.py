from django.shortcuts import render
from django.shortcuts import redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
import simplejson as json
from .utils import generate_order_number, check_callback
from django.http import HttpResponse
import requests
import time
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    cart_amounts = get_cart_amounts(request)  # Call the function once and store the results
    subtotal = cart_amounts['subtotal']
    total_tax = cart_amounts['tax']
    tax_data = cart_amounts['tax_dict']
    grand_total = cart_amounts['grand_total']
    print(tax_data)
    print(subtotal, total_tax, grand_total)
    
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.email = form.cleaned_data['email']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.county = form.cleaned_data['county']
            order.city = form.cleaned_data['city']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            context ={
                'order': order,
                'cart_items': cart_items,
            }
            return render(request, 'orders/place_order.html', context)
        
            
                    
        else:
            print(form.errors)
        
    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    
        # check if request is ajax or not
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # get the payment method
            order_number = request.POST.get('order_number')
            transaction_id = request.POST.get('transaction_id')
            payment_method = request.POST.get('payment_method')
            status = request.POST.get('status')
            print(order_number, transaction_id, payment_method, status)
            
            order = Order.objects.get(order_number=order_number, user=request.user)
            
            payment = Payment(
                user = request.user,
                transaction_id = transaction_id,
                payment_method = payment_method,
                amount = order.total,
                status = status   
            )
            payment.save()
            
            order.payment = payment
            order.is_ordered = True
            order.save()
            
            
            cart_items = Cart.objects.filter(user=request.user)
            
            for item in cart_items:
                ordered_food = OrderedFood()
                ordered_food.order = order
                ordered_food.payment = payment
                ordered_food.user = request.user
                
                ordered_food.fooditem = item.fooditem
                ordered_food.quantity = item.quantity
                ordered_food.price = item.fooditem.price
                ordered_food.amount = item.fooditem.price * item.quantity
                ordered_food.save()
            
            
            mail_subject = 'Thank you for ordering with us'
            mail_template = 'orders/order_confirmation.html'
            context = {
                'order': order,
                'user': request.user,
                'to_email': order.email,
            }
            send_notification(mail_subject, mail_template, context)
            
            # mail_subject = 'You have recieved a new order'
            # mail_template = 'orders/new_order.html'
            # to_emails = []
            # for i in cart_items:
            #     if i.fooditem.vendor.user.email not in to_emails:
            #         to_emails.append(i.fooditem.vendor.user.email)
                    
            
            # print(to_emails)
            # context = {
            #     'order': order,
            #     'user': request.user,
            #     'to_email': to_emails,
            # }
            
            # send_notification(mail_subject, mail_template, context)
            
            # cart_items.delete()
            
            return HttpResponse('success')
        

        return HttpResponse('payment successful')
       


