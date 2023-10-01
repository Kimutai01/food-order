from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.shortcuts import redirect
from vendor.models import OpeningHour
from datetime import date
from datetime import datetime
from orders.forms import OrderForm
from accounts.models import Profile



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
    
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=date.today().isoweekday())
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        
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
                    return JsonResponse({'status': 'success', 'message': 'Increased product quantity', 'cart_counter': get_cart_counter(request), 'qty': cart_item.quantity, 'cart_amounts': get_cart_amounts(request)})
                except:
                    cart_item = Cart.objects.create(
                        user=request.user,
                        fooditem=fooditem,
                        quantity=1,
                    )
                    cart_item.save()
                    return JsonResponse({'status': 'success', 'message': 'Added to cart','cart_counter': get_cart_counter(request),'qty': cart_item.quantity, 'cart_amounts': get_cart_amounts(request)})
                    
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
                        return JsonResponse({'status': 'success', 'message': 'Decreased product quantity', 'cart_counter': get_cart_counter(request), 'qty': cart_item.quantity, 'cart_amounts': get_cart_amounts(request)})
                    else:
                        cart_item.delete()
                        return JsonResponse({'status': 'success', 'message': 'Removed from cart', 'cart_counter': get_cart_counter(request), 'qty': 0, 'cart_amounts': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This food does not exist in your cart'})
                    
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})
                
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please Log in to continue'})
    
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'Removed from cart', 'cart_counter': get_cart_counter(request), 'cart_amounts': get_cart_amounts(request)})
                else:
                    return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist in your cart'})
            
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
        
def search(request):
    
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']

        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
        print(fetch_vendors_by_fooditems)
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
            
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
                profile__location__distance_lte=(pnt, D(km=radius))
                ).annotate(distance=Distance("profile__location", pnt)).order_by("distance")
            
            for v in vendors:
                v.kms = round(v.distance.km, 1)
                
        vendor_count = vendors.count()
                
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address,
        }
        
    return render(request, 'marketplace/listings.html', context)

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    profile = Profile.objects.get(user=request.user)
    default_values={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': request.user.phone_number,
        'address': profile.address,
        'country': profile.country,
        'county': profile.county,
        'city': profile.city,
    }
    print(default_values)
    form = OrderForm(initial=default_values)
    
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    # if request.method == 'POST':
    #     form = OrderForm(request.POST, initial=default_values)
    #     if form.is_valid():
    #         order = form.save(commit=False)
    #         order.user = request.user
    #         order.save()
    #         return redirect('home')
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)
        
        

