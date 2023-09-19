from django.db import models
from accounts.models import User, Profile
from accounts.utils import send_notification
from datetime import time
from datetime import datetime
from datetime import date

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor',null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name
    
    def is_open(self):
        # Check current day's opening hours.
        today_date = date.today()
        
        today = today_date.isoweekday()
        
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open

    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                template = 'clinic_approved.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                        
                if self.is_approved:
                    # send email to vendor
                    subject = 'Your vetinary clinic has been approved!'
                    send_notification(subject,template,context)
                else:
                    # send email to vendor
                    subject='Unfortunately, you are not elligible to be listed as a vetinary clinic'   
                    send_notification(subject,template,context)
                
        return super(Vendor, self).save(*args, **kwargs)
  
       
    



DAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True, null=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day', 'from_hour']
        unique_together = ('day', 'from_hour', 'to_hour')
        
    def __str__(self):
        return self.get_day_display()
    

class Appointment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ('vendor', 'date', 'time')
        
    def __str__(self):
        return self.user.first_name + ' - ' + str(self.date) + ' ' + str(self.time)
    

class DoctorNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    note = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return self.note

    
    
