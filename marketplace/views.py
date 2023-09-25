from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Cart
from .context_processors import get_cart_counter



# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(
        is_approved=True,
        user__is_active=True,
    )
    context = {
        'vendors': vendors,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True),
        )
    ) 
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
    if(request.user.is_authenticated):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
        
                    # Check if user has already added to the cart
                try:
                    cart_item = Cart.objects.get(
                        user=request.user,
                        fooditem=fooditem,
                    )
                    cart_item.quantity += 1
                    cart_item.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased product quantity', 'cart_counter': get_cart_counter(request), 'qty': cart_item.quantity})
                except:
                    cart_item = Cart.objects.create(
                        user=request.user,
                        fooditem=fooditem,
                        quantity=1,
                    )
                    cart_item.save()
                    return JsonResponse({'status': 'success', 'message': 'Added to cart','cart_counter': get_cart_counter(request),'qty': cart_item.quantity})
                    
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})
                
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please Log in to continue'})
    
def decrease_cart(request, food_id):
    if(request.user.is_authenticated):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
        
                    # Check if user has already added to the cart
                try:
                    cart_item = Cart.objects.get(
                        user=request.user,
                        fooditem=fooditem,
                    )
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        return JsonResponse({'status': 'success', 'message': 'Decreased product quantity', 'cart_counter': get_cart_counter(request), 'qty': cart_item.quantity})
                    else:
                        cart_item.delete()
                        return JsonResponse({'status': 'success', 'message': 'Removed from cart', 'cart_counter': get_cart_counter(request), 'qty': 0})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This food does not exist in your cart'})
                    
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})
                
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please Log in to continue'})
    
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)
