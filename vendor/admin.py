from django.contrib import admin
from .models import Vendor, OpeningHour, Appointment, DoctorNote

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_name', 'user', 'is_approved', 'created_at']
    list_display_links = ['vendor_name', 'user']
    list_editable = ['is_approved']
    
class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'day', 'from_hour', 'to_hour']

   

admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)
admin.site.register(Appointment)
admin.site.register(DoctorNote)
