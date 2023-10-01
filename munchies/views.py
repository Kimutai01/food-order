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
        headers = {
            "Content-Type": "application/json",
            "Api-Key": "pk_0b51e48bc6ac135ce3f65b1355248cae71ef085c0223bc0273535a4e174dce07",
        }

        payload = {
            "customer_details": {
                "full_name": "Albert Chela",
                "location": "Nairobi",
                "phone_number": "254790841979",
                "email": "alber@chpter.co",
            },
            "products": [
                {
                    "product_name": "HoodEez",
                    "quantity": 1,
                    "unit_price": 1,
                    "digital_link": "https://example.com/link",
                }
            ],
            "amount": {
                "currency": "KES",
                "delivery_fee": 0.00,
                "discount_fee": 0.00,
                "total": 1.00,
            },
            "callback_details": {
                "notify_customer": True,
                "transaction_reference": "1234",
                "callback_url": "https://thekultureke.com/api/mpesa_transactions",
            },
        }

        json_payload = json.dumps(payload)
        url = 'https://api.chpter.co/v1/initiate/mpesa-payment'
        response = requests.post(url, headers=headers, data=json_payload)

        # Now you can handle the response from the API as needed.
        if response.status_code == 200:
            print("Request successful")
            print("Response:", response.json())
        else:
            print("Request failed with status code:", response.status_code)
            print("Response:", response.text)
    return render(request, 'chapter.html')