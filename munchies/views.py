from django.shortcuts import render, HttpResponse
from vendor.models import Vendor
import requests
import json
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else:
        return None
        



def home(request):
    if get_or_set_current_location(request):
        
        pnt = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))
        
            
        vendors = Vendor.objects.filter(
            profile__location__distance_lte=(pnt, D(km=1000))
            ).annotate(distance=Distance("profile__location", pnt)).order_by("distance")
            
        for v in vendors:
            v.kms = round(v.distance.km, 1)
            
    else:
   
        vendors = Vendor.objects.filter(
            
            is_approved=True,
            user__is_active=True,      
        
        )[:5]
        print(vendors)

    context = {
        'vendors': vendors,
    }

    
    
    return render(request, 'home.html', context)

def chapter(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        print(name)
        print(email)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer your_token_here'
        }


        payload = {
        'name': 'John Doe',
        'email': 'johndoe@example.com'
        }

        json_payload = json.dumps(payload)
        url = 'https://api.example.com/endpoint'
        response = requests.post(url, headers=headers, data=json_payload)
    return render(request, 'chapter.html')