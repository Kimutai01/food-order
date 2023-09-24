from django.shortcuts import render, HttpResponse
from vendor.models import Vendor
import requests
import json

# def get_or_set_current_location(request):
#     if 'lat' in request.session and 'lng' in request.session:
#         return 'juja'
#     elif 'lat' in request.GET and 'lng' in request.GET:
#         return 'juja'
#     else:
#         return ''



def home(request):
   
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