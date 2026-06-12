from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def create_or_update_instructor_profile(sender, instance, created, **kwargs):
    if instance.is_instructor:
        InstructorProfile.objects.get_or_create(user=instance)



        