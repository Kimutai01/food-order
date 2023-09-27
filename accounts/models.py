from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from twilio.rest import Client

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (RESTAURANT, 'restaurant'),
        (CUSTOMER, 'customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    
    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'restaurant'
        elif self.role == 2:
            user_role = 'customer'
        return user_role
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, default='profiles/default-user.png')
    cover_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, default='profiles/default-cover.png')
    address = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    location = gis_models.PointField(srid=4326, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if(self.longitude and self.latitude):
            self.location = Point(float(self.longitude), float(self.latitude))
            return super(Profile, self).save(*args, **kwargs)
        return super(Profile, self).save(*args, **kwargs)
    
    
    # def full_address(self):
    #     return f'{self.address_line_1} {self.address_line_2}'
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # send text message
    #     account_sid = ''
    #     auth_token = ''
    #     client = Client(account_sid, auth_token)
        
    #     message = client.messages.create(
    #         body='Your profile has been created successfully',
    #         from_='+13345083906',
    #         to='+254790841979'
    #     )
    
    #     print(message.sid)
        
    #     return super().save(*args, **kwargs)
    


# post_save.connect(create_user_profile, sender=User)
