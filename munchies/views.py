from django.shortcuts import render, HttpResponse
from vendor.models import Vendor


def get_or_set_current_location(request):
    if 'lat' in request.session and 'lng' in request.session:
        return 'juja'
    elif 'lat' in request.GET and 'lng' in request.GET:
        return 'juja'
    else:
        return ''



def home(request):
    city = get_or_set_current_location(request)
    clinics = Vendor.objects.filter(
        
        is_approved=True,
        user__is_active=True,
       #check if profile.city == city
        user__profile__city__icontains=city
        
        
       
    )[:5]

    context = {
        'clinics': clinics
    }

    # clinics = Vendor.objects.filter(is_approved=True, user__is_active=True)[:5]
    # print(clinics)
    
    # context = {
    #     'clinics': clinics
    # }
    
    return render(request, 'home.html', context)