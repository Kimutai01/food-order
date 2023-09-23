from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch

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
    print(categories)
    context = {
        'vendor': vendor,
        'categories': categories,
        
    }
    return render(request, 'marketplace/vendor_detail.html', context)
