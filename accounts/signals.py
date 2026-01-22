from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, UserRole


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created"""
    if created:
        # Get or create the default 'user' role
        user_role, _ = UserRole.objects.get_or_create(
            role_name='user',
            defaults={
                'description': 'Regular user with basic permissions'
            }
        )
        UserProfile.objects.create(user=instance, role=user_role)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        user_role, _ = UserRole.objects.get_or_create(
            role_name='user',
            defaults={
                'description': 'Regular user with basic permissions'
            }
        )
        UserProfile.objects.create(user=instance, role=user_role)
