from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        Profile.objects.create(user=instance)
        print("Profile created!")
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
            print("Profile updated!")
        except:
            Profile.objects.create(user=instance)
            print("Profile created!")
         
